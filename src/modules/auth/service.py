"""Authentication Services."""

from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import jwt
from jwt import PyJWTError

from src.config import settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .exceptions import AuthenticationError, DuplicateEmailError, InvalidCredentialError
from .schemas import LoginUserRequest, RegisterUserRequest, TokenData, Token
from src.models.user import User

import logging

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return bcrypt_context.hash(password)


def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    """Authenticate a user by their email and password."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication attempt for user {email}")
        return False
    return user


def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    """Create a JWT access token."""
    encode = {"sub": email, "id": str(user_id), "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenData:
    """Verify a JWT token and extract the token data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        return TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.error(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def register_user(db: Session, register_user_request: RegisterUserRequest) -> None:
    """Register a new user."""
    try:
        existing_user = db.query(User).filter(User.email == register_user_request.email).first()
        if existing_user:
            raise DuplicateEmailError(register_user_request.email)

        create_user_model = User(
            firstname=register_user_request.first_name,
            lastname=register_user_request.last_name,
            email=register_user_request.email,
            password_hash=get_password_hash(register_user_request.password),
        )
        db.add(create_user_model)
        db.commit()

    except DuplicateEmailError:
        raise
    except Exception as e:
        raise AuthenticationError(f"Registration failed: {str(e)}")


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    """Get current user from token."""
    return verify_token(token)


CurrentUser = Annotated[TokenData, Depends(get_current_user)]


def login_user_access_token(form_data: LoginUserRequest, db: Session) -> Token:
    """Authenticate user and return access token."""
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise InvalidCredentialError()
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(email=user.email, user_id=user.id, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
