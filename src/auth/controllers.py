"""This module provides authentication routes for the application."""

from fastapi import APIRouter, Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
import entities
import services

from ..database.core import DbSession
from ..core import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

# endpoint to register a new user
@router.post("/", status_code=HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register_user(request: Request, db: DbSession, register_user_request: entities.RegisterUserRequest):
    services.register_user(db, register_user_request)
    return {"message": "User registered successfully."}

# endpoint to login a user and get an access token
@router.post("/token", response_model=entities.Token, status_code=HTTP_200_OK)
async def login_user_access_token(form_data: entities.LoginUserRequest, db: DbSession):
    return services.login_user_access_token(form_data, db)