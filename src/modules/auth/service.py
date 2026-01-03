"""Authentication Services."""
import re

from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import jwt
from jwt import PyJWTError

from src.config import settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .exceptions import AuthenticationError, DuplicateEmailError, InvalidCredentialError
from .schemas import RegisterUserRequest, TokenData, Token
from src.models.user import User
from src.models.otp import OTPPurpose

import logging

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
MAX_BCRYPT_BYTES = settings.MAX_BCRYPT_BYTES

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return (
        len(password) >= 12 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*()]", password)
    )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    plain_bytes = plain_password.encode("utf-8")[:MAX_BCRYPT_BYTES]
    return bcrypt_context.verify( plain_bytes.decode("utf-8", errors="ignore"),
        hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    # bcrypt requires <= 72 bytes
    password_bytes = password.encode("utf-8")
    safe_password = password_bytes[:MAX_BCRYPT_BYTES]
    return bcrypt_context.hash(safe_password.decode("utf-8", errors="ignore"))

def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    """Authenticate a user by their email and password."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication attempt for user {email}")
        return False
    return user


def create_access_token(email: str, user_id: UUID, role: str, expires_delta: timedelta) -> str:
    """Create a JWT access token."""
    encode = {"sub": email, "id": str(user_id), "role": role, "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenData:
    """Verify a JWT token and extract the token data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        role: str = payload.get("role")
        return TokenData(user_id=user_id, role=role)
    except PyJWTError as e:
        logging.error(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def register_user(db: Session, register_user_request: RegisterUserRequest) -> User:
    """Register a new user and send welcome + verification emails."""
    # Import here to avoid circular imports
    from src.modules.notifications.service import send_welcome_notification_helper
    from src.modules.otps.service import OTPService
    
    try:
        existing_user = db.query(User).filter(User.email == register_user_request.email).first()
        if existing_user:
            raise DuplicateEmailError(register_user_request.email)
        #validate the password strength
        if not validate_password(register_user_request.password):
            raise AuthenticationError("Password does not meet strength requirements.")
        
        #create the user
        create_user_model = User(
            firstname=register_user_request.first_name,
            lastname=register_user_request.last_name,
            email=register_user_request.email,
            role=register_user_request.role,
            password_hash=get_password_hash(register_user_request.password),
        )
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)
        
        # Send welcome notification
        try:
            send_welcome_notification_helper(db, create_user_model.id)
            logging.info(f"Welcome notification sent to user {create_user_model.id}")
        except Exception as e:
            logging.error(f"Failed to send welcome notification: {str(e)}")
        
        # Generate and send email verification OTP
        try:
            otp_service = OTPService(db)
            otp_service.create_otp(
                user_id=create_user_model.id,
                purpose=OTPPurpose.EMAIL_VERIFICATION,
                max_attempts=3,
                send_notification=True  # This will send the email verification notification
            )
            logging.info(f"Email verification OTP sent to user {create_user_model.id}")
        except Exception as e:
            logging.error(f"Failed to send email verification OTP: {str(e)}")
        
        return create_user_model

    except DuplicateEmailError:
        raise
    except Exception as e:
        raise AuthenticationError(f"Registration failed: {str(e)}")


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    """Get current user from token."""
    return verify_token(token)


def require_admin(current_user: TokenData) -> TokenData:
    """Verify that the current user has admin role."""
    if not current_user.is_admin():
        from fastapi import HTTPException
        from starlette.status import HTTP_403_FORBIDDEN
        logging.warning(f"Non-admin user {current_user.user_id} attempted admin action")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )
    return current_user


def get_admin_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    """Get current user from token and verify admin role."""
    current_user = verify_token(token)
    return require_admin(current_user)


CurrentUser = Annotated[TokenData, Depends(get_current_user)]
AdminUser = Annotated[TokenData, Depends(get_admin_user)]


def login_user_access_token(form_data: OAuth2PasswordRequestForm, db: Session) -> Token:
    """Authenticate user and return access token.
    
    Note: OAuth2PasswordRequestForm uses 'username' field, which we use for email.
    """
    # OAuth2 spec uses 'username', we use email as the username
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise InvalidCredentialError()
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(email=user.email, user_id=user.id, role=user.role.value, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", role=user.role.value)
