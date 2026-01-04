"""Tests for OTP service - validating OTP generation and notification for all purposes."""

import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from unittest.mock import patch, MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database import Base
from src.models.user import User
from src.models.otp import OTP, OTPPurpose
from src.modules.otps.service import OTPService, OTPMessages
from src.modules.auth.service import get_password_hash


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test_otp.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user in the database."""
    user = User(
        id=uuid4(),
        firstname="Test",
        lastname="User",
        email="testuser@example.com",
        password_hash=get_password_hash("Test@Password123!"),
        role="user",
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestOTPGeneration:
    """Tests for OTP generation functionality."""

    def test_generate_otp_code_format(self, db_session):
        """Test that generated OTP codes have correct format (6 digits)."""
        service = OTPService(db_session)
        code = service.generate_otp_code()
        
        assert len(code) == 6
        assert code.isdigit()

    def test_generate_otp_code_randomness(self, db_session):
        """Test that generated OTP codes are random."""
        service = OTPService(db_session)
        codes = [service.generate_otp_code() for _ in range(10)]
        
        # Check that not all codes are the same
        assert len(set(codes)) > 1


class TestOTPCreation:
    """Tests for OTP creation with notifications for each purpose."""

    @patch('src.modules.notifications.service.send_login_otp_notification_helper')
    def test_create_otp_login_sends_notification(self, mock_notification, db_session, test_user):
        """Test that LOGIN OTP creation sends login notification."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=True
        )
        
        assert otp is not None
        assert otp.purpose == OTPPurpose.LOGIN
        assert otp.user_id == test_user.id
        assert not otp.is_used
        mock_notification.assert_called_once()
        call_args = mock_notification.call_args
        assert call_args[0][1] == test_user.id  # user_id
        assert len(call_args[0][2]) == 6  # otp_code (6 digits)

    @patch('src.modules.notifications.service.send_transaction_otp_notification_helper')
    def test_create_otp_transaction_sends_notification(self, mock_notification, db_session, test_user):
        """Test that TRANSACTION OTP creation sends transaction notification."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.TRANSACTION,
            send_notification=True
        )
        
        assert otp is not None
        assert otp.purpose == OTPPurpose.TRANSACTION
        mock_notification.assert_called_once()

    @patch('src.modules.notifications.service.send_password_reset_otp_notification_helper')
    def test_create_otp_password_reset_sends_notification(self, mock_notification, db_session, test_user):
        """Test that PASSWORD_RESET OTP creation sends password reset notification."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.PASSWORD_RESET,
            send_notification=True
        )
        
        assert otp is not None
        assert otp.purpose == OTPPurpose.PASSWORD_RESET
        mock_notification.assert_called_once()

    @patch('src.modules.notifications.service.send_email_verification_notification_helper')
    def test_create_otp_email_verification_sends_notification(self, mock_notification, db_session, test_user):
        """Test that EMAIL_VERIFICATION OTP creation sends email verification notification."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            send_notification=True
        )
        
        assert otp is not None
        assert otp.purpose == OTPPurpose.EMAIL_VERIFICATION
        mock_notification.assert_called_once()

    @patch('src.modules.notifications.service.send_otp_notification_helper')
    def test_create_otp_phone_verification_sends_generic_notification(self, mock_notification, db_session, test_user):
        """Test that PHONE_VERIFICATION OTP creation sends generic notification."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.PHONE_VERIFICATION,
            send_notification=True
        )
        
        assert otp is not None
        assert otp.purpose == OTPPurpose.PHONE_VERIFICATION
        mock_notification.assert_called_once()

    @patch('src.modules.notifications.service.send_otp_notification_helper')
    def test_create_otp_account_activation_sends_generic_notification(self, mock_notification, db_session, test_user):
        """Test that ACCOUNT_ACTIVATION OTP creation sends generic notification."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.ACCOUNT_ACTIVATION,
            send_notification=True
        )
        
        assert otp is not None
        assert otp.purpose == OTPPurpose.ACCOUNT_ACTIVATION
        mock_notification.assert_called_once()

    def test_create_otp_without_notification(self, db_session, test_user):
        """Test that OTP can be created without sending notification."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=False
        )
        
        assert otp is not None
        # No notification should be sent when send_notification=False


class TestOTPVerification:
    """Tests for OTP verification functionality."""

    def test_verify_valid_otp(self, db_session, test_user):
        """Test verification of a valid OTP."""
        service = OTPService(db_session)
        
        # Create OTP without notification
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=False
        )
        
        # Verify OTP
        result = service.verify_otp(otp, otp.code)
        
        assert result is True
        assert otp.is_used is True
        assert otp.used_at is not None

    def test_verify_invalid_otp_code(self, db_session, test_user):
        """Test verification with invalid code."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.TRANSACTION,
            send_notification=False
        )
        
        result = service.verify_otp(otp, "000000")
        
        assert result is False
        assert otp.is_used is False
        assert otp.attempts == 1

    def test_verify_expired_otp(self, db_session, test_user):
        """Test verification of expired OTP."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.PASSWORD_RESET,
            send_notification=False
        )
        
        # Manually expire the OTP
        otp.expires_at = datetime.now(timezone.utc) - timedelta(minutes=5)
        db_session.commit()
        
        result = service.verify_otp(otp, otp.code)
        
        assert result is False

    def test_verify_already_used_otp(self, db_session, test_user):
        """Test verification of already used OTP."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            send_notification=False
        )
        
        # Use the OTP
        service.verify_otp(otp, otp.code)
        
        # Try to use again
        result = service.verify_otp(otp, otp.code)
        
        assert result is False

    def test_verify_max_attempts_exceeded(self, db_session, test_user):
        """Test that OTP becomes invalid after max attempts."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            max_attempts=3,
            send_notification=False
        )
        
        # Make 3 failed attempts
        for _ in range(3):
            service.verify_otp(otp, "000000")
        
        # Now even correct code should fail
        result = service.verify_otp(otp, otp.code)
        
        assert result is False
        assert otp.attempts >= 3


class TestOTPValidity:
    """Tests for OTP validity checking."""

    def test_is_valid_fresh_otp(self, db_session, test_user):
        """Test that a fresh OTP is valid."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.TRANSACTION,
            send_notification=False
        )
        
        assert service.is_valid(otp) is True

    def test_is_valid_used_otp(self, db_session, test_user):
        """Test that a used OTP is not valid."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=False
        )
        
        otp.is_used = True
        db_session.commit()
        
        assert service.is_valid(otp) is False

    def test_is_valid_expired_otp(self, db_session, test_user):
        """Test that an expired OTP is not valid."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.PASSWORD_RESET,
            send_notification=False
        )
        
        otp.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        db_session.commit()
        
        assert service.is_valid(otp) is False


class TestOTPInvalidation:
    """Tests for OTP invalidation when creating new ones."""

    def test_create_new_otp_invalidates_old(self, db_session, test_user):
        """Test that creating a new OTP invalidates existing ones for same purpose."""
        service = OTPService(db_session)
        
        # Create first OTP
        otp1 = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=False
        )
        otp1_code = otp1.code
        
        # Create second OTP for same purpose
        otp2 = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=False
        )
        
        # Refresh otp1 from database
        db_session.refresh(otp1)
        
        # Old OTP should be invalidated (marked as used)
        assert otp1.is_used is True
        
        # New OTP should be valid
        assert service.is_valid(otp2) is True


class TestOTPResponseMessages:
    """Tests for OTP response message generation."""

    def test_generate_otp_response_success(self, db_session, test_user):
        """Test successful OTP generation response."""
        service = OTPService(db_session)
        
        with patch.object(service, '_send_otp_notification'):
            response = service.generate_otp_response(
                user_id=test_user.id,
                purpose=OTPPurpose.TRANSACTION
            )
        
        assert response.message == OTPMessages.GENERATED_SUCCESS
        assert response.purpose == OTPPurpose.TRANSACTION
        assert response.expires_at is not None

    def test_verify_otp_response_success(self, db_session, test_user):
        """Test successful OTP verification response."""
        service = OTPService(db_session)
        
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            send_notification=False
        )
        
        response = service.verify_user_otp_response(
            user_id=test_user.id,
            code=otp.code,
            purpose=OTPPurpose.EMAIL_VERIFICATION
        )
        
        assert response.success is True
        assert response.message == OTPMessages.VERIFIED_SUCCESS

    def test_verify_otp_response_invalid(self, db_session, test_user):
        """Test invalid OTP verification response."""
        service = OTPService(db_session)
        
        service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=False
        )
        
        response = service.verify_user_otp_response(
            user_id=test_user.id,
            code="000000",
            purpose=OTPPurpose.LOGIN
        )
        
        assert response.success is False

    def test_verify_otp_response_no_active_otp(self, db_session, test_user):
        """Test verification response when no active OTP exists."""
        service = OTPService(db_session)
        
        response = service.verify_user_otp_response(
            user_id=test_user.id,
            code="123456",
            purpose=OTPPurpose.TRANSACTION
        )
        
        assert response.success is False
        assert response.message == OTPMessages.NO_ACTIVE_OTP
