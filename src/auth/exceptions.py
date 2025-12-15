"""Exceptions for auth app"""

from fastapi import HTTPException


class UserError(HTTPException):
    """Base exception for user-related errors"""

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

    def __init__(self, message: str = "Email or password are incorrect"):
        super().__init__(status_code=404, detail=message)
