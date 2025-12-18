from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    password: Optional[str] = None


class UserResponseModel(UserBase):
    id: UUID

    class Config:
        from_attributes = True
        orm_mode = True


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
