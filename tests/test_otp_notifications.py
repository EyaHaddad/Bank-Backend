"""Tests for OTP notification service - validating email content for all OTP purposes."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4
from unittest.mock import patch, MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database import Base
from src.models.user import User
from src.models.notification import Notification
from src.modules.auth.service import get_password_hash


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test_notification.db"
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
        firstname="Jean",
        lastname="Dupont",
        email="jean.dupont@example.com",
        password_hash=get_password_hash("Test@Password123!"),
        role="user",
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestOTPNotificationContent:
    """Tests for OTP notification email content generation."""

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_login_otp_notification_content(self, mock_smtp, db_session, test_user):
        """Test that LOGIN OTP notification has correct content."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        otp_code = "123456"
        
        # Mock SMTP
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = service.send_login_otp_notification(test_user.id, otp_code)
        
        assert notification is not None
        assert "Login Verification" in notification.title or "login" in notification.content.lower()
        assert otp_code in notification.content
        assert test_user.firstname in notification.content

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_transaction_otp_notification_content(self, mock_smtp, db_session, test_user):
        """Test that TRANSACTION OTP notification has correct content."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        otp_code = "654321"
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = service.send_transaction_otp_notification(test_user.id, otp_code)
        
        assert notification is not None
        assert "Transaction" in notification.title or "transaction" in notification.content.lower()
        assert otp_code in notification.content

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_password_reset_otp_notification_content(self, mock_smtp, db_session, test_user):
        """Test that PASSWORD_RESET OTP notification has correct content."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        otp_code = "789012"
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = service.send_password_reset_otp_notification(test_user.id, otp_code)
        
        assert notification is not None
        assert "Password" in notification.title or "password" in notification.content.lower()
        assert otp_code in notification.content

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_email_verification_notification_content(self, mock_smtp, db_session, test_user):
        """Test that EMAIL_VERIFICATION OTP notification has correct content."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        otp_code = "246810"
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = service.send_email_verification_notification(test_user.id, otp_code)
        
        assert notification is not None
        assert otp_code in notification.content


class TestOTPNotificationHelpers:
    """Tests for OTP notification helper functions."""

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_send_login_otp_notification_helper(self, mock_smtp, db_session, test_user):
        """Test the login OTP notification helper function."""
        from src.modules.notifications.service import send_login_otp_notification_helper
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = send_login_otp_notification_helper(db_session, test_user.id, "111111")
        
        assert notification is not None
        assert notification.user_id == test_user.id

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_send_transaction_otp_notification_helper(self, mock_smtp, db_session, test_user):
        """Test the transaction OTP notification helper function."""
        from src.modules.notifications.service import send_transaction_otp_notification_helper
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = send_transaction_otp_notification_helper(db_session, test_user.id, "222222")
        
        assert notification is not None
        assert notification.user_id == test_user.id

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_send_password_reset_otp_notification_helper(self, mock_smtp, db_session, test_user):
        """Test the password reset OTP notification helper function."""
        from src.modules.notifications.service import send_password_reset_otp_notification_helper
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = send_password_reset_otp_notification_helper(db_session, test_user.id, "333333")
        
        assert notification is not None
        assert notification.user_id == test_user.id

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_send_email_verification_notification_helper(self, mock_smtp, db_session, test_user):
        """Test the email verification notification helper function."""
        from src.modules.notifications.service import send_email_verification_notification_helper
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        notification = send_email_verification_notification_helper(db_session, test_user.id, "444444")
        
        assert notification is not None
        assert notification.user_id == test_user.id


class TestEmailContentGeneration:
    """Tests for email content generation methods."""

    def test_generate_login_otp_content(self, db_session):
        """Test login OTP email content generation."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        user_name = "Jean Dupont"
        otp_code = "123456"
        
        subject, content = service._generate_login_otp_content(user_name, otp_code)
        
        assert "Login" in subject or "Verification" in subject
        assert user_name in content
        assert otp_code in content
        assert "5 minutes" in content

    def test_generate_transaction_otp_content(self, db_session):
        """Test transaction OTP email content generation."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        user_name = "Marie Martin"
        otp_code = "654321"
        
        subject, content = service._generate_transaction_otp_content(user_name, otp_code)
        
        assert "Transaction" in subject
        assert user_name in content
        assert otp_code in content
        assert "transaction" in content.lower()

    def test_generate_password_reset_otp_content(self, db_session):
        """Test password reset OTP email content generation."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        user_name = "Pierre Bernard"
        otp_code = "789012"
        
        subject, content = service._generate_password_reset_otp_content(user_name, otp_code)
        
        assert "Password" in subject or "Reset" in subject
        assert user_name in content
        assert otp_code in content
        assert "password" in content.lower()

    def test_generate_email_verification_content(self, db_session):
        """Test email verification OTP content generation."""
        from src.modules.notifications.service import NotificationService
        
        service = NotificationService(db_session)
        user_name = "Sophie Leroy"
        otp_code = "246810"
        
        subject, content = service._generate_email_verification_content(user_name, otp_code)
        
        assert "Verification" in subject or "Email" in subject
        assert user_name in content
        assert otp_code in content


class TestOTPNotificationIntegration:
    """Integration tests for OTP creation with notification sending."""

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_otp_service_sends_login_notification(self, mock_smtp, db_session, test_user):
        """Test that OTPService correctly sends login notification."""
        from src.modules.otps.service import OTPService
        from src.models.otp import OTPPurpose
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        service = OTPService(db_session)
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.LOGIN,
            send_notification=True
        )
        
        assert otp is not None
        # Verify SMTP was called (email was sent)
        assert mock_smtp.called

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_otp_service_sends_transaction_notification(self, mock_smtp, db_session, test_user):
        """Test that OTPService correctly sends transaction notification."""
        from src.modules.otps.service import OTPService
        from src.models.otp import OTPPurpose
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        service = OTPService(db_session)
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.TRANSACTION,
            send_notification=True
        )
        
        assert otp is not None
        assert mock_smtp.called

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_otp_service_sends_password_reset_notification(self, mock_smtp, db_session, test_user):
        """Test that OTPService correctly sends password reset notification."""
        from src.modules.otps.service import OTPService
        from src.models.otp import OTPPurpose
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        service = OTPService(db_session)
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.PASSWORD_RESET,
            send_notification=True
        )
        
        assert otp is not None
        assert mock_smtp.called

    @patch('src.modules.notifications.service.smtplib.SMTP')
    def test_otp_service_sends_email_verification_notification(self, mock_smtp, db_session, test_user):
        """Test that OTPService correctly sends email verification notification."""
        from src.modules.otps.service import OTPService
        from src.models.otp import OTPPurpose
        
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        
        service = OTPService(db_session)
        otp = service.create_otp(
            user_id=test_user.id,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            send_notification=True
        )
        
        assert otp is not None
        assert mock_smtp.called
