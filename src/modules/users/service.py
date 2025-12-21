"""User services module for user-related operations."""

from uuid import UUID
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import schemas
from src.models.user import User
from src.modules.auth.exceptions import (
    InvalidPasswordError,
    PasswordMismatchError,
    UserNotFoundError,
    DuplicateEmailError,
)
from src.modules.auth.service import get_password_hash, verify_password

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    def list_users(self) -> list[User]:
        """Retrieve all users from the database."""
        logger.debug("Fetching all users from database")
        users = self._db.query(User).all()
        logger.info(f"Retrieved {len(users)} users")
        return users

    def get_user(self, user_id: UUID) -> User | None:
        """Retrieve a user by their ID."""
        logger.debug(f"Fetching user with ID: {user_id}")
        return self._db.query(User).filter(User.id == user_id).first()

    def get_user_by_id(self, user_id: UUID) -> User:
        """Retrieve a user by ID, raising exception if not found."""
        user = self.get_user(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address."""
        logger.debug(f"Fetching user with email: {email}")
        return self._db.query(User).filter(User.email == email).first()

    def create_user(self, user: schemas.UserCreate) -> User:
        """Create a new user in the database."""
        logger.info(f"Attempting to create user with email: {user.email}")

        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            logger.warning(f"Duplicate email registration attempt: {user.email}")
            raise DuplicateEmailError(user.email)

        try:
            new_user = User(
                firstname=user.firstname,
                lastname=user.lastname,
                email=user.email,
                password_hash=get_password_hash(user.password),
            )
            self._db.add(new_user)
            self._db.commit()
            self._db.refresh(new_user)
            logger.info(f"Successfully created user with ID: {new_user.id}")
            return new_user
        except IntegrityError as e:
            self._db.rollback()
            logger.error(f"Database integrity error creating user: {str(e)}")
            raise DuplicateEmailError(user.email)

    def update_user(self, user_id: UUID, user_data: schemas.UserUpdate) -> User:
        """Update a user's information."""
        user = self.get_user_by_id(user_id)

        if user_data.firstname:
            user.firstname = user_data.firstname
        if user_data.lastname:
            user.lastname = user_data.lastname
        if user_data.password:
            user.password_hash = get_password_hash(user_data.password)

        self._db.commit()
        self._db.refresh(user)
        logger.info(f"Successfully updated user with ID: {user_id}")
        return user

    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user from the database."""
        user = self.get_user_by_id(user_id)
        self._db.delete(user)
        self._db.commit()
        logger.info(f"Successfully deleted user with ID: {user_id}")
        return True

    def change_password(self, user_id: UUID, password_data: schemas.PasswordChange) -> None:
        """Change a user's password."""
        if password_data.new_password != password_data.new_password_confirm:
            raise PasswordMismatchError()

        user = self.get_user_by_id(user_id)

        if not verify_password(password_data.current_password, user.password_hash):
            raise InvalidPasswordError()

        user.password_hash = get_password_hash(password_data.new_password)
        self._db.commit()
        logger.info(f"Successfully changed password for user with ID: {user_id}")
