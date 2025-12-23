"""Admin schemas - Pydantic models for request/response."""

from uuid import UUID
from pydantic import BaseModel


class PromoteUserRequest(BaseModel):
    """Model for promoting a user to admin."""
    user_id: UUID


class PromoteUserResponse(BaseModel):
    """Model for promote user response."""
    message: str
    user_id: UUID
    new_role: str
