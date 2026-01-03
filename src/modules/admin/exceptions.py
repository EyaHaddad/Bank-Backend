"""Admin module exceptions."""

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN


class AdminAccessDeniedError(HTTPException):
    """Exception raised when a non-admin user tries to access admin-only endpoints."""
    
    def __init__(self):
        super().__init__(
            status_code=HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )


# Note: User and Account exceptions have been moved to their respective modules:
# - UserNotFoundError, UserAlreadyActiveError, etc. -> src/modules/auth/exceptions.py
# - AccountNotFoundError, AccountAlreadyActiveError, etc. -> src/modules/accounts/exceptions.py
