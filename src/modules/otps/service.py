"""OTP services module for OTP-related operations."""

from datetime import datetime, timedelta, timezone
from uuid import UUID
import secrets
import logging

from sqlalchemy.orm import Session

from src.config import settings
from src.models.otp import OTP, OTPPurpose
from src.models.user import User
from .schemas import OTPGenerateResponse, OTPVerifyResponse

logger = logging.getLogger(__name__)

OTP_VALIDITY_SECONDS = settings.OTP_VALIDITY_PERIOD * 60
OTP_DIGITS = settings.OTP_DIGITS


# OTP Messages
class OTPMessages:
    """Centralized OTP response messages."""
    GENERATED_SUCCESS = "OTP generated and sent successfully"
    VERIFIED_SUCCESS = "OTP verified successfully"
    INVALID_OR_EXPIRED = "Invalid or expired OTP code"
    NO_ACTIVE_OTP = "No active OTP found for this purpose"
    MAX_ATTEMPTS_EXCEEDED = "Maximum verification attempts exceeded"
    OTP_ALREADY_USED = "This OTP has already been used"


class OTPService:
    """Service class for OTP-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    def generate_otp_code(self) -> str:
        """Generate a random OTP and its expiration time."""

        return "".join([str(secrets.randbelow(10)) for _ in range(OTP_DIGITS)])

    def is_valid(self, otp: OTP) -> bool:
        """Check if OTP is still valid."""
        if otp.is_used:
            logger.debug(f"OTP {otp.id} is already used")
            return False
        if otp.attempts >= otp.max_attempts:
            logger.debug(f"OTP {otp.id} has exceeded max attempts")
            return False
        if datetime.now(timezone.utc) > otp.expires_at.replace(tzinfo=timezone.utc):
            logger.debug(f"OTP {otp.id} has expired")
            return False
        return True

    def verify_otp(self, otp: OTP, code: str) -> bool:
        """Verify the OTP code and update attempts counter."""
        otp.attempts += 1
        
        if not self.is_valid(otp):
            self._db.commit()
            return False
        
        if otp.code == code:
            otp.is_used = True
            otp.used_at = datetime.now(timezone.utc)
            self._db.commit()
            logger.info(f"OTP {otp.id} verified successfully")
            return True
        
        self._db.commit()
        logger.warning(f"OTP {otp.id} verification failed - invalid code")
        return False

    def create_otp(self, user_id: UUID, purpose: OTPPurpose, max_attempts: int = 3, send_notification: bool = True) -> OTP:
        """Create a new OTP for a user and optionally send notification."""
        logger.info(f"Creating OTP for user {user_id} with purpose {purpose}")
        
        # Invalidate any existing unused OTPs for the same purpose
        self._invalidate_existing_otps(user_id, purpose)
        
        code = self.generate_otp_code()
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=OTP_VALIDITY_SECONDS)
        
        otp = OTP(
            user_id=user_id,
            code=code,
            purpose=purpose,
            expires_at=expires_at,
            max_attempts=max_attempts,
        )
        
        self._db.add(otp)
        self._db.commit()
        self._db.refresh(otp)
        
        logger.info(f"OTP created with ID: {otp.id}")
        
        # Send email notification based on purpose
        if send_notification:
            self._send_otp_notification(user_id, code, purpose)
        
        return otp

    def _send_otp_notification(self, user_id: UUID, otp_code: str, purpose: OTPPurpose) -> None:
        """Send email notification for OTP based on its purpose."""
        # Import here to avoid circular imports
        from src.modules.notifications.service import (
            send_otp_notification_helper,
            send_email_verification_notification_helper,
            send_login_otp_notification_helper,
            send_transaction_otp_notification_helper,
            send_password_reset_otp_notification_helper,
        )
        
        try:
            if purpose == OTPPurpose.EMAIL_VERIFICATION:
                send_email_verification_notification_helper(self._db, user_id, otp_code)
            elif purpose == OTPPurpose.LOGIN:
                send_login_otp_notification_helper(self._db, user_id, otp_code)
            elif purpose == OTPPurpose.TRANSACTION:
                send_transaction_otp_notification_helper(self._db, user_id, otp_code)
            elif purpose == OTPPurpose.PASSWORD_RESET:
                send_password_reset_otp_notification_helper(self._db, user_id, otp_code)
            else:
                # For other purposes (PHONE_VERIFICATION, ACCOUNT_ACTIVATION), use generic OTP notification
                send_otp_notification_helper(self._db, user_id, otp_code)
            logger.info(f"OTP notification sent for purpose {purpose} to user {user_id}")
        except Exception as e:
            # Log error but don't fail OTP creation
            logger.error(f"Failed to send OTP notification for user {user_id}: {str(e)}")

    def generate_otp_response(self, user_id: UUID, purpose: OTPPurpose, max_attempts: int = 3) -> OTPGenerateResponse:
        """Create a new OTP and return a response schema."""
        otp = self.create_otp(user_id, purpose, max_attempts)
        return OTPGenerateResponse(
            message=OTPMessages.GENERATED_SUCCESS,
            expires_at=otp.expires_at,
            purpose=otp.purpose,
        )

    def verify_user_otp_response(self, user_id: UUID, code: str, purpose: OTPPurpose) -> OTPVerifyResponse:
        """Verify an OTP and return a response schema with appropriate message."""
        otp = self.get_active_otp(user_id, purpose)
        
        if not otp:
            logger.warning(f"No active OTP found for user {user_id} with purpose {purpose}")
            return OTPVerifyResponse(success=False, message=OTPMessages.NO_ACTIVE_OTP)
        
        if otp.is_used:
            return OTPVerifyResponse(success=False, message=OTPMessages.OTP_ALREADY_USED)
        
        if otp.attempts >= otp.max_attempts:
            return OTPVerifyResponse(success=False, message=OTPMessages.MAX_ATTEMPTS_EXCEEDED)
        
        is_valid = self.verify_otp(otp, code)
        
        if is_valid:
            return OTPVerifyResponse(success=True, message=OTPMessages.VERIFIED_SUCCESS)
        else:
            return OTPVerifyResponse(success=False, message=OTPMessages.INVALID_OR_EXPIRED)

    def _invalidate_existing_otps(self, user_id: UUID, purpose: OTPPurpose) -> None:
        """Invalidate all existing unused OTPs for a user and purpose."""
        existing_otps = (
            self._db.query(OTP)
            .filter(
                OTP.user_id == user_id,
                OTP.purpose == purpose,
                OTP.is_used == False,
            )
            .all()
        )
        
        for otp in existing_otps:
            otp.is_used = True
            logger.debug(f"Invalidated existing OTP: {otp.id}")
        
        self._db.commit()

    def get_otp_by_id(self, otp_id: UUID) -> OTP | None:
        """Retrieve an OTP by its ID."""
        return self._db.query(OTP).filter(OTP.id == otp_id).first()

    def get_active_otp(self, user_id: UUID, purpose: OTPPurpose) -> OTP | None:
        """Get the most recent active OTP for a user and purpose."""
        otp = (
            self._db.query(OTP)
            .filter(
                OTP.user_id == user_id,
                OTP.purpose == purpose,
                OTP.is_used == False,
            )
            .order_by(OTP.created_at.desc())
            .first()
        )
        
        if otp and self.is_valid(otp):
            return otp
        return None

    def verify_user_otp(self, user_id: UUID, code: str, purpose: OTPPurpose) -> bool:
        """Verify an OTP for a user with a specific purpose."""
        otp = self.get_active_otp(user_id, purpose)
        
        if not otp:
            logger.warning(f"No active OTP found for user {user_id} with purpose {purpose}")
            return False
        
        return self.verify_otp(otp, code)

    def get_user_otps(self, user_id: UUID, limit: int = 10) -> list[OTP]:
        """Retrieve recent OTPs for a user."""
        return (
            self._db.query(OTP)
            .filter(OTP.user_id == user_id)
            .order_by(OTP.created_at.desc())
            .limit(limit)
            .all()
        )

    def cleanup_expired_otps(self) -> int:
        """Delete all expired OTPs. Returns the count of deleted OTPs."""
        now = datetime.now(timezone.utc)
        result = (
            self._db.query(OTP)
            .filter(OTP.expires_at < now)
            .delete(synchronize_session=False)
        )
        self._db.commit()
        logger.info(f"Cleaned up {result} expired OTPs")
        return result
