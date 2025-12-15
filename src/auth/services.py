"""Authentication Services"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from uuid import UUID, uuid4
import jwt
from jwt import PyJWTError

from ..core.config import settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .exceptions import AuthenticationError, DuplicateEmailError, InvalidCredentialError
from .models import LoginUserRequest, RegisterUserRequest, TokenData, Token
from src.models.user import User

import logging

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    :param plain_password: The plain password to verify
    :param hashed_password: The hashed password to compare against
    :returns: True if the password matches, False otherwise
    """
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.

    :param password: The plain password to hash
    :returns: The hashed password
    """
    return bcrypt_context.hash(password)


def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    """
    Authenticate a user by their email and password.

    :param email: The user's email
    :param password: The user's password
    :param db: Database session
    :returns: The authenticated user
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        logging.warning(f"Failed authentication attempt for user {email}")
        return False
    return user


def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    """
    Create a JWT access token.

    :param email: The user's email
    :param user_id: The user's ID
    :param expires_delta: The token's expiration time
    :returns: The JWT access token
    """
    encode = {"sub": email, "id": str(user_id), "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenData:
    """
    Verify a JWT token and extract the token data.

    :param token: The JWT token to verify
    :returns: The token data
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        return TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.error(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def register_user(db: Session, register_user_request: RegisterUserRequest) -> None:
    """
    Register a new user.

    :param db: Database session
    :param register_user_request: Data for the new user
    :raises DuplicateEmailError: If the email is already registered
    :raises AuthenticationError: If registration fails for other reasons
    """
    try:
        existing_user = db.query(User).filter(User.email == register_user_request.email).first()
        if existing_user:
            raise DuplicateEmailError(register_user_request.email)

        create_user_model = User(
            first_name=register_user_request.firstname,
            last_name=register_user_request.lastname,
            email=register_user_request.email,
            hashed_password=get_password_hash(register_user_request.password),
        )
        db.add(create_user_model)
        db.commit()

    except DuplicateEmailError:
        # Re-raise DuplicateEmailError
        raise
    except Exception as e:
        # Log the exception or handle it specifically
        raise AuthenticationError(f"Registration failed: {str(e)}")


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    return verify_token(token)

CurrentUser = Annotated[TokenData, Depends(get_current_user)]


def login_user_access_token(form_data: LoginUserRequest, 
                            db: Session)-> Token:
    
    """
    Authenticate user and return access token.

    :param form_data: User login data
    :param db: Database session
    :returns: Access token and token type
    :raises InvalidCredentialError: If authentication fails
    """
    user = authenticate_user(form_data.email, form_data.password, db) 
    if not user:
        raise InvalidCredentialError()
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(email=user.email, user_id=user.id, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
