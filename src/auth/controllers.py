"""This module provides authentication routes for the application."""

from fastapi import APIRouter, Request

import src.auth.services as auth_services
from src.auth.models import LoginUserRequest

from ..database.core import DbSession
from ..utils import build_response
from .models import RegisterUserRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/")
async def register_user(request: Request, db: DbSession, register_user_request: RegisterUserRequest):
    auth_services.register_user(db, register_user_request)
    return build_response(success=True, message="User registered successfully", status_code=201)


@router.post("/token")
async def login_user_access_token(form_data: LoginUserRequest, db: DbSession):
    token = auth_services.login_user_access_token(form_data, db)
    return build_response(success=True, message="Login successful", data=token.model_dump(), status_code=200)
