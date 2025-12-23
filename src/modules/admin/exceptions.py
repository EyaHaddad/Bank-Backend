"""Admin module exceptions."""

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


class AdminAccessDeniedError(HTTPException):
    """Exception raised when a non-admin user tries to access admin-only endpoints."""
    
    def __init__(self):
        super().__init__(
            status_code=HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )


class UserNotFoundError(HTTPException):
    """Exception raised when the target user is not found."""
    
    def __init__(self, user_id: str):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )


class UserAlreadyAdminError(HTTPException):
    """Exception raised when trying to promote a user who is already an admin."""
    
    def __init__(self, user_id: str):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} is already an admin."
        )
