"""Authentication router - API endpoints for auth operations."""

from fastapi import APIRouter, Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from . import schemas
from . import service

from src.infrastructure.database import DbSession
from src.infrastructure.security.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register_user(
    request: Request,
    db: DbSession,
    register_user_request: schemas.RegisterUserRequest
):
    """Register a new user."""
    service.register_user(db, register_user_request)
    return {"message": "User registered successfully."}


@router.post("/token", response_model=schemas.Token, status_code=HTTP_200_OK)
async def login_user_access_token(
    form_data: schemas.LoginUserRequest,
    db: DbSession
):
    """Login and get an access token."""
    return service.login_user_access_token(form_data, db)
