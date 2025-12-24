"""Notification services module for notification-related operations."""

import logging
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.config import settings
from src.models.notification import Notification, NotificationType
from src.models.user import User

from .exceptions import (
    NotificationNotFoundError,
    NotificationSendError,
    UserNotFoundForNotificationError,
)
from .schemas import (
    SendOTPNotificationRequest,
    SendTransactionNotificationRequest,
    SendBankNewsNotificationRequest,
    CreateNotificationRequest,
)

logger = logging.getLogger(__name__)


class NotificationService:
    """Service class for notification-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    # ==================== Email Template Methods ====================

    def _generate_otp_email_content(self, otp_code: str, user_name: str) -> tuple[str, str]:
        """Generate email subject and content for OTP notification."""
        subject = "Your Secure Banking OTP Code"
        content = f"""
Dear {user_name},

Your One-Time Password (OTP) for secure authentication is:

    {otp_code}

This code is valid for 5 minutes. Do not share this code with anyone.

If you did not request this code, please contact our support team immediately.

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_transaction_email_content(
        self,
        user_name: str,
        transaction_type: str,
        amount: float,
        account_number: Optional[str] = None,
        reference: Optional[str] = None,
    ) -> tuple[str, str]:
        """Generate email subject and content for transaction notification."""
        action = "credited to" if transaction_type.lower() == "credit" else "debited from"
        subject = f"Transaction Alert: {transaction_type.capitalize()} of ${amount:.2f}"
        
        account_info = f" (Account: ...{account_number[-4:]})" if account_number else ""
        ref_info = f"\nReference: {reference}" if reference else ""
        
        content = f"""
Dear {user_name},

This is to inform you that a transaction has been processed on your account.

Transaction Details:
- Type: {transaction_type.capitalize()}
- Amount: ${amount:.2f} {action} your account{account_info}
- Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC{ref_info}

If you did not authorize this transaction, please contact our support team immediately.

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_news_email_content(self, title: str, news_content: str, user_name: str) -> tuple[str, str]:
        """Generate email subject and content for bank news notification."""
        subject = f"Bank News: {title}"
        content = f"""
Dear {user_name},

{news_content}

Thank you for banking with us.

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_welcome_email_content(self, user_name: str, email: str) -> tuple[str, str]:
        """Generate email subject and content for welcome/registration notification."""
        subject = "Welcome to Secure Banking!"
        content = f"""
Dear {user_name},

Welcome to Secure Banking! Your account has been successfully created.

Account Details:
- Email: {email}
- Registration Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC

For your security, please verify your email address using the verification code sent separately.

Important Security Tips:
- Never share your password or OTP codes with anyone
- Always log out when using shared devices
- Contact our support team if you notice any suspicious activity

Thank you for choosing Secure Banking!

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_email_verification_content(self, user_name: str, otp_code: str) -> tuple[str, str]:
        """Generate email subject and content for email verification OTP."""
        subject = "Verify Your Email Address - Secure Banking"
        content = f"""
Dear {user_name},

Please verify your email address to complete your registration.

Your Email Verification Code is:

    {otp_code}

This code is valid for 10 minutes. Do not share this code with anyone.

If you did not create an account with us, please ignore this email or contact our support team.

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_password_change_content(self, user_name: str) -> tuple[str, str]:
        """Generate email subject and content for password change notification."""
        subject = "Password Changed Successfully - Secure Banking"
        content = f"""
Dear {user_name},

Your password has been successfully changed on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC.

If you did not make this change, please contact our support team immediately and secure your account.

Security Recommendations:
- Use a strong, unique password
- Enable two-factor authentication
- Regularly review your account activity

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_login_otp_content(self, user_name: str, otp_code: str) -> tuple[str, str]:
        """Generate email subject and content for login OTP notification."""
        subject = "Your Login Verification Code - Secure Banking"
        content = f"""
Dear {user_name},

A login attempt was made to your account. Please use the following code to verify your identity:

    {otp_code}

This code is valid for 5 minutes. Do not share this code with anyone.

If you did not attempt to log in, please secure your account immediately and contact our support team.

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_transaction_otp_content(self, user_name: str, otp_code: str) -> tuple[str, str]:
        """Generate email subject and content for transaction OTP notification."""
        subject = "Transaction Verification Code - Secure Banking"
        content = f"""
Dear {user_name},

A transaction has been initiated from your account. Please use the following code to authorize this transaction:

    {otp_code}

This code is valid for 5 minutes. Do not share this code with anyone.

If you did not initiate this transaction, please cancel it immediately and contact our support team.

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    def _generate_password_reset_otp_content(self, user_name: str, otp_code: str) -> tuple[str, str]:
        """Generate email subject and content for password reset OTP notification."""
        subject = "Password Reset Verification Code - Secure Banking"
        content = f"""
Dear {user_name},

A password reset was requested for your account. Please use the following code to reset your password:

    {otp_code}

This code is valid for 10 minutes. Do not share this code with anyone.

If you did not request a password reset, please ignore this email and ensure your account is secure.

Best regards,
Your Banking Team
        """.strip()
        return subject, content

    # ==================== Core Methods ====================

    def _get_user_by_id(self, user_id: UUID) -> User:
        """Retrieve a user by ID."""
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundForNotificationError(user_id)
        return user

    def _create_notification_record(
        self,
        user_id: UUID,
        title: str,
        content: str,
        notification_type: NotificationType = NotificationType.EMAIL,
    ) -> Notification:
        """Create and persist a notification record in the database."""
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            content=content,
            sent_at=datetime.now(timezone.utc),
        )
        self._db.add(notification)
        self._db.commit()
        self._db.refresh(notification)
        return notification

    def _send_email_notification(self, to_email: str, subject: str, content: str) -> bool:
        """Send an email notification using SMTP."""
        try:
            msg = EmailMessage()
            # Set email headers and content
            msg["From"] = settings.SMTP_FROM_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.set_content(content)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise NotificationSendError(f"Failed to send email: {str(e)}")

    # ==================== Public Service Methods ====================

    def send_otp_notification(self, request: SendOTPNotificationRequest) -> Notification:
        """Send an OTP notification via email."""
        user = self._get_user_by_id(request.user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_otp_email_content(request.otp_code, user_name)
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"OTP notification sent to user {user.id}")
        return notification

    def send_transaction_notification(self, request: SendTransactionNotificationRequest) -> Notification:
        """Send a transaction notification via email."""
        user = self._get_user_by_id(request.user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_transaction_email_content(
            user_name=user_name,
            transaction_type=request.transaction_type,
            amount=request.amount,
            account_number=request.account_number,
            reference=request.reference,
        )
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"Transaction notification sent to user {user.id}")
        return notification

    def send_bank_news_notification(
        self, request: SendBankNewsNotificationRequest
    ) -> list[Notification]:
        """Send a bank news notification to one user or all users."""
        notifications = []
        
        if request.user_id:
            # Send to specific user
            user = self._get_user_by_id(request.user_id)
            user_name = f"{user.firstname} {user.lastname}"
            subject, content = self._generate_news_email_content(
                request.title, request.content, user_name
            )
            
            try:
                self._send_email_notification(user.email, subject, content)
                notification = self._create_notification_record(
                    user_id=user.id,
                    title=subject,
                    content=content,
                )
                notifications.append(notification)
            except NotificationSendError as e:
                logger.error(f"Failed to send news to user {user.id}: {str(e)}")
                raise
        else:
            # Send to all active users
            users = self._db.query(User).filter(User.is_active.is_(True)).all()
            for user in users:
                user_name = f"{user.firstname} {user.lastname}"
                subject, content = self._generate_news_email_content(
                    request.title, request.content, user_name
                )
                
                try:
                    self._send_email_notification(user.email, subject, content)
                    notification = self._create_notification_record(
                        user_id=user.id,
                        title=subject,
                        content=content,
                    )
                    notifications.append(notification)
                except NotificationSendError as e:
                    logger.error(f"Failed to send news to user {user.id}: {str(e)}")
                    # Continue with other users even if one fails
                    continue
        
        logger.info(f"Bank news notification sent to {len(notifications)} user(s)")
        return notifications

    def create_notification(self, request: CreateNotificationRequest) -> Notification:
        """Create a custom notification and send via email."""
        user = self._get_user_by_id(request.user_id)
        
        # Send email
        self._send_email_notification(user.email, request.title, request.content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=request.title,
            content=request.content,
        )
        
        logger.info(f"Custom notification sent to user {user.id}")
        return notification

    def get_notification_by_id(self, notification_id: UUID) -> Notification:
        """Retrieve a notification by its ID."""
        notification = (
            self._db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )
        if not notification:
            raise NotificationNotFoundError(notification_id)
        return notification

    def get_user_notifications(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Notification], int]:
        """Retrieve all notifications for a user with pagination."""
        # Verify user exists
        self._get_user_by_id(user_id)
        
        query = (
            self._db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.sent_at.desc())
        )
        
        total = query.count()
        notifications = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return notifications, total

    def delete_notification(self, notification_id: UUID, user_id: UUID) -> bool:
        """Delete a notification by its ID (user must own the notification)."""
        notification = (
            self._db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
            .first()
        )
        if not notification:
            raise NotificationNotFoundError(notification_id)
        
        self._db.delete(notification)
        self._db.commit()
        
        logger.info(f"Notification {notification_id} deleted by user {user_id}")
        return True

    # ==================== Additional Public Service Methods ====================

    def send_welcome_notification(self, user_id: UUID) -> Notification:
        """Send a welcome email notification to a newly registered user."""
        user = self._get_user_by_id(user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_welcome_email_content(user_name, user.email)
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"Welcome notification sent to user {user.id}")
        return notification

    def send_email_verification_notification(self, user_id: UUID, otp_code: str) -> Notification:
        """Send an email verification OTP notification."""
        user = self._get_user_by_id(user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_email_verification_content(user_name, otp_code)
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"Email verification notification sent to user {user.id}")
        return notification

    def send_password_change_notification(self, user_id: UUID) -> Notification:
        """Send a password change confirmation notification."""
        user = self._get_user_by_id(user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_password_change_content(user_name)
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"Password change notification sent to user {user.id}")
        return notification

    def send_login_otp_notification(self, user_id: UUID, otp_code: str) -> Notification:
        """Send a login OTP notification."""
        user = self._get_user_by_id(user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_login_otp_content(user_name, otp_code)
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"Login OTP notification sent to user {user.id}")
        return notification

    def send_transaction_otp_notification(self, user_id: UUID, otp_code: str) -> Notification:
        """Send a transaction OTP notification."""
        user = self._get_user_by_id(user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_transaction_otp_content(user_name, otp_code)
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"Transaction OTP notification sent to user {user.id}")
        return notification

    def send_password_reset_otp_notification(self, user_id: UUID, otp_code: str) -> Notification:
        """Send a password reset OTP notification."""
        user = self._get_user_by_id(user_id)
        user_name = f"{user.firstname} {user.lastname}"
        
        subject, content = self._generate_password_reset_otp_content(user_name, otp_code)
        
        # Send email
        self._send_email_notification(user.email, subject, content)
        
        # Create notification record
        notification = self._create_notification_record(
            user_id=user.id,
            title=subject,
            content=content,
        )
        
        logger.info(f"Password reset OTP notification sent to user {user.id}")
        return notification


# ==================== Helper Functions for External Use ====================


def send_otp_notification_helper(db: Session, user_id: UUID, otp_code: str) -> Notification:
    """Helper function to send OTP notification from other modules."""
    service = NotificationService(db)
    request = SendOTPNotificationRequest(user_id=user_id, otp_code=otp_code)
    return service.send_otp_notification(request)


def send_transaction_notification_helper(
    db: Session,
    user_id: UUID,
    transaction_type: str,
    amount: float,
    account_number: Optional[str] = None,
    reference: Optional[str] = None,
) -> Notification:
    """Helper function to send transaction notification from other modules."""
    service = NotificationService(db)
    request = SendTransactionNotificationRequest(
        user_id=user_id,
        transaction_type=transaction_type,
        amount=amount,
        account_number=account_number,
        reference=reference,
    )
    return service.send_transaction_notification(request)


def send_welcome_notification_helper(db: Session, user_id: UUID) -> Notification:
    """Helper function to send welcome notification from other modules."""
    service = NotificationService(db)
    return service.send_welcome_notification(user_id)


def send_email_verification_notification_helper(
    db: Session, user_id: UUID, otp_code: str
) -> Notification:
    """Helper function to send email verification notification from other modules."""
    service = NotificationService(db)
    return service.send_email_verification_notification(user_id, otp_code)


def send_password_change_notification_helper(db: Session, user_id: UUID) -> Notification:
    """Helper function to send password change notification from other modules."""
    service = NotificationService(db)
    return service.send_password_change_notification(user_id)


def send_login_otp_notification_helper(
    db: Session, user_id: UUID, otp_code: str
) -> Notification:
    """Helper function to send login OTP notification from other modules."""
    service = NotificationService(db)
    return service.send_login_otp_notification(user_id, otp_code)


def send_transaction_otp_notification_helper(
    db: Session, user_id: UUID, otp_code: str
) -> Notification:
    """Helper function to send transaction OTP notification from other modules."""
    service = NotificationService(db)
    return service.send_transaction_otp_notification(user_id, otp_code)


def send_password_reset_otp_notification_helper(
    db: Session, user_id: UUID, otp_code: str
) -> Notification:
    """Helper function to send password reset OTP notification from other modules."""
    service = NotificationService(db)
    return service.send_password_reset_otp_notification(user_id, otp_code)
