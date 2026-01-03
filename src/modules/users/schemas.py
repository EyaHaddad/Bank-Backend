"""User schemas - Pydantic models for request/response."""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

from src.models.user import Role


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None
    role: Role = Role.USER


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    password: Optional[str] = None


class UserResponseModel(UserBase):
    id: UUID
    phone: Optional[str] = None
    role: Role
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
