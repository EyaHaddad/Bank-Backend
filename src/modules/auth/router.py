"""Authentication router - API endpoints for auth operations."""

import logging
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST

from . import schemas
from . import service
from .pending_registration import pending_registrations

from src.infrastructure.database import DbSession
from src.infrastructure.security.rate_limiter import limiter
from src.models.otp import OTPPurpose
from src.models.user import User
from src.modules.otps.service import OTPService, OTPMessages

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=HTTP_201_CREATED)
@limiter.limit("100/minute")
async def register_user(
    request: Request,
    db: DbSession,
    register_user_request: schemas.RegisterUserRequest
):
    """
    Initiate user registration - stores data temporarily until OTP verification.
    User is NOT created in the database until email is verified.
    """
    # Check if email already exists in database
    existing_user = db.query(User).filter(User.email == register_user_request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password
    if not service.validate_password(register_user_request.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Password must be at least 12 characters and include uppercase, lowercase, number, and special character (!@#$%^&*())"
        )
    
    # Validate passwords match
    if register_user_request.password != register_user_request.confirm_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Hash password and store pending registration
    password_hash = service.get_password_hash(register_user_request.password)
    otp_code = pending_registrations.add(
        first_name=register_user_request.first_name,
        last_name=register_user_request.last_name,
        email=register_user_request.email,
        phone=None,  # Add phone if needed
        password_hash=password_hash,
        role=register_user_request.role
    )
    
    # Send OTP email
    try:
        from src.modules.notifications.service import send_email_verification_otp
        send_email_verification_otp(register_user_request.email, otp_code)
        logger.info(f"OTP sent to {register_user_request.email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email: {e}")
        # Still return success - OTP is stored, user can request resend
    
    return {"message": "Verification code sent to your email. Please verify to complete registration."}


@router.post("/verify-email", response_model=schemas.VerifyEmailResponse, status_code=HTTP_200_OK)
@limiter.limit("100/minute")
async def verify_email(
    request: Request,
    db: DbSession,
    verify_request: schemas.VerifyEmailRequest
):
    """
    Verify email with OTP code and complete registration.
    Creates the user in the database only after successful verification.
    """
    # Get pending registration
    pending = pending_registrations.get(verify_request.email)
    if not pending:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No pending registration found. Please register again."
        )
    
    # Check if OTP is expired
    if pending.is_otp_expired():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Verification code has expired. Please request a new one."
        )
    
    # Verify OTP
    if not pending.verify_otp(verify_request.code):
        remaining = pending.max_attempts - pending.attempts
        if remaining <= 0:
            pending_registrations.remove(verify_request.email)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Too many failed attempts. Please register again."
            )
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Invalid verification code. {remaining} attempts remaining."
        )
    
    # OTP verified - now create the user in the database
    try:
        # Check again if email exists (race condition protection)
        existing_user = db.query(User).filter(User.email == pending.email).first()
        if existing_user:
            pending_registrations.remove(verify_request.email)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user with verified email
        new_user = User(
            firstname=pending.first_name,
            lastname=pending.last_name,
            email=pending.email,
            phone=pending.phone,
            password_hash=pending.password_hash,
            role=pending.role,
            is_email_verified=True,  # Already verified!
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Remove pending registration
        pending_registrations.remove(verify_request.email)
        
        # Send welcome notification
        try:
            from src.modules.notifications.service import send_welcome_notification_helper
            send_welcome_notification_helper(db, new_user.id)
            logger.info(f"Welcome notification sent to user {new_user.id}")
        except Exception as e:
            logger.error(f"Failed to send welcome notification: {e}")
        
        return schemas.VerifyEmailResponse(
            success=True,
            message="Email verified successfully. You can now sign in."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create user after OTP verification: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Failed to complete registration. Please try again."
        )


@router.post("/resend-otp", status_code=HTTP_200_OK)
@limiter.limit("3/minute")
async def resend_otp(
    request: Request,
    db: DbSession,
    resend_request: schemas.ResendOTPRequest
):
    """Resend email verification OTP for pending registration."""
    # Get pending registration
    pending = pending_registrations.get(resend_request.email)
    if not pending:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No pending registration found. Please register again."
        )
    
    # Regenerate OTP
    new_otp = pending_registrations.regenerate_otp(resend_request.email)
    if not new_otp:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Registration expired. Please register again."
        )
    
    # Send OTP email
    try:
        from src.modules.notifications.service import send_email_verification_otp
        send_email_verification_otp(resend_request.email, new_otp)
        logger.info(f"Resent OTP to {resend_request.email}")
    except Exception as e:
        logger.error(f"Failed to resend OTP email: {e}")
    
    return {"message": "Verification code sent successfully"}


@router.post("/token", response_model=schemas.Token, status_code=HTTP_200_OK)
async def login_user_access_token(
    db: DbSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Login and get an access token. Use email as username."""
    # Check if user exists and email is verified
    user = db.query(User).filter(User.email == form_data.username).first()
    if user and not user.is_email_verified:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Please verify your email before logging in"
        )
    
    return service.login_user_access_token(form_data, db)


@router.post("/forgot-password", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
async def forgot_password(
    request: Request,
    db: DbSession,
    forgot_request: schemas.ForgotPasswordRequest
):
    """
    Request a password reset OTP.
    Sends an OTP to the user's email for password reset.
    """
    # Check if user exists
    user = db.query(User).filter(User.email == forgot_request.email).first()
    if not user:
        # Return success even if user doesn't exist (security - don't reveal if email exists)
        logger.warning(f"Password reset requested for non-existent email: {forgot_request.email}")
        return {"message": "If this email exists, a password reset code has been sent."}
    
    # Generate and send OTP
    try:
        otp_service = OTPService(db)
        otp_service.create_otp(
            user_id=user.id,
            purpose=OTPPurpose.PASSWORD_RESET,
            max_attempts=3,
            send_notification=True
        )
        logger.info(f"Password reset OTP sent to user {user.id}")
    except Exception as e:
        logger.error(f"Failed to send password reset OTP: {e}")
    
    return {"message": "If this email exists, a password reset code has been sent."}


@router.post("/reset-password", response_model=schemas.ResetPasswordResponse, status_code=HTTP_200_OK)
@limiter.limit("10/minute")
async def reset_password(
    request: Request,
    db: DbSession,
    reset_request: schemas.ResetPasswordRequest
):
    """
    Reset password using OTP verification.
    Validates the OTP and updates the user's password.
    """
    # Validate passwords match
    if reset_request.new_password != reset_request.confirm_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Validate password strength
    if not service.validate_password(reset_request.new_password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Password must be at least 12 characters and include uppercase, lowercase, number, and special character (!@#$%^&*())"
        )
    
    # Find user
    user = db.query(User).filter(User.email == reset_request.email).first()
    if not user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid email or verification code"
        )
    
    # Verify OTP
    otp_service = OTPService(db)
    result = otp_service.verify_user_otp_response(
        user_id=user.id,
        code=reset_request.code,
        purpose=OTPPurpose.PASSWORD_RESET
    )
    
    if not result.success:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=result.message
        )
    
    # Update password
    try:
        user.password_hash = service.get_password_hash(reset_request.new_password)
        db.commit()
        
        # Send password change notification
        try:
            from src.modules.notifications.service import send_password_change_notification_helper
            send_password_change_notification_helper(db, user.id)
        except Exception as e:
            logger.error(f"Failed to send password change notification: {e}")
        
        logger.info(f"Password reset successful for user {user.id}")
        return schemas.ResetPasswordResponse(
            success=True,
            message="Password reset successfully. You can now sign in with your new password."
        )
    except Exception as e:
        logger.error(f"Failed to reset password: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Failed to reset password. Please try again."
        )
