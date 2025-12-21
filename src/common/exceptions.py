"""Base exceptions for common error handling."""

from fastapi import HTTPException


class BaseError(HTTPException):
    """Base exception for application errors."""
    pass
