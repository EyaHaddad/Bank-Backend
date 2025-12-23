"""Exceptions for notifications module."""

from fastapi import HTTPException


class NotificationError(HTTPException):
    """Base exception for notification-related errors."""
    pass


class NotificationNotFoundError(NotificationError):
    """Exception raised when a notification is not found."""

    def __init__(self, notification_id=None):
        message = (
            "Notification not found"
            if notification_id is None
            else f"Notification with id {notification_id} not found"
        )
        super().__init__(status_code=404, detail=message)


class NotificationSendError(NotificationError):
    """Exception raised when a notification fails to send."""

    def __init__(self, reason: str = "Failed to send notification"):
        super().__init__(status_code=500, detail=reason)


class InvalidNotificationTypeError(NotificationError):
    """Exception raised when an invalid notification type is provided."""

    def __init__(self, notification_type: str = None):
        message = (
            "Invalid notification type"
            if notification_type is None
            else f"Invalid notification type: {notification_type}"
        )
        super().__init__(status_code=400, detail=message)


class UserNotFoundForNotificationError(NotificationError):
    """Exception raised when a user is not found for sending a notification."""

    def __init__(self, user_id=None):
        message = (
            "User not found for notification"
            if user_id is None
            else f"User with id {user_id} not found for notification"
        )
        super().__init__(status_code=404, detail=message)
