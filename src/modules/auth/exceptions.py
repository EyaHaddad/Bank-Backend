"""Exceptions for auth module."""

from fastapi import HTTPException


class UserError(HTTPException):
    """Base exception for user-related errors."""
    pass


class UserNotFoundError(UserError):
    """Exception raised when a user is not found."""

    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)


class PasswordMismatchError(UserError):
    """Exception raised when new passwords do not match."""

    def __init__(self):
        super().__init__(status_code=400, detail="New passwords do not match")


class InvalidPasswordError(UserError):
    """Exception raised when the current password is incorrect."""

    def __init__(self):
        super().__init__(status_code=401, detail="Current password is incorrect")


class DuplicateEmailError(UserError):
    """Exception raised when trying to register with an email that already exists."""

    def __init__(self, email: str = None):
        message = "Email already exists" if email is None else f"User with email {email} already exists"
        super().__init__(status_code=409, detail=message)


class AuthenticationError(HTTPException):
    """Exception raised for authentication failures."""

    def __init__(self, message: str = "Could not validate user"):
        super().__init__(status_code=401, detail=message)


class InvalidCredentialError(HTTPException):
    """Exception raised for authentication failures."""

    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials")


class UserAlreadyActiveError(UserError):
    """Exception raised when trying to activate an already active user."""

    def __init__(self, user_id=None):
        message = "User is already active" if user_id is None else f"User {user_id} is already active"
        super().__init__(status_code=400, detail=message)


class UserAlreadyInactiveError(UserError):
    """Exception raised when trying to deactivate an already inactive user."""

    def __init__(self, user_id=None):
        message = "User is already inactive" if user_id is None else f"User {user_id} is already inactive"
        super().__init__(status_code=400, detail=message)


class CannotModifySelfError(UserError):
    """Exception raised when a user tries to modify their own account in restricted ways."""

    def __init__(self, action: str = "perform this action on"):
        super().__init__(status_code=400, detail=f"Cannot {action} your own account")
