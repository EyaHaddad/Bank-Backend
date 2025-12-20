"""User services module for user-related operations.

This module contains all the business logic related to users: CRUD operations,
password management, and user validation.
"""
from uuid import UUID
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models
from src.entities.user import User
from src.auth.exceptions import (
    InvalidPasswordError,
    PasswordMismatchError,
    UserNotFoundError,
    DuplicateEmailError,
)
from src.auth.services import get_password_hash, verify_password

# Configure module-level logger
logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations.
    
    This service handles all user CRUD operations and password management,
    with proper exception handling and logging.
    """
    
    def __init__(self, session: Session):
        """Initialize the service with a database session.
        
        Args:
            session: SQLAlchemy database session for database operations.
        """
        self._db = session

    def list_users(self) -> list[User]:
        """Retrieve all users from the database.
        
        Returns:
            List of all User entities.
        """
        logger.debug("Fetching all users from database")
        users = self._db.query(User).all()
        logger.info(f"Retrieved {len(users)} users")
        return users

    def get_user(self, user_id: UUID) -> User | None:
        """Retrieve a user by their ID.
        
        Args:
            user_id: The UUID of the user to retrieve.
            
        Returns:
            The User entity if found, None otherwise.
        """
        logger.debug(f"Fetching user with ID: {user_id}")
        return self._db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.
        
        Args:
            email: The email address of the user to retrieve.
            
        Returns:
            The User entity if found, None otherwise.
        """
        logger.debug(f"Fetching user with email: {email}")
        return self._db.query(User).filter(User.email == email).first()

    def create_user(self, user: models.UserCreate) -> User:
        """Create a new user in the database.
        
        Args:
            user: UserCreate model containing user data.
            
        Returns:
            The created User entity.
            
        Raises:
            DuplicateEmailError: If a user with the same email already exists.
        """
        logger.info(f"Attempting to create user with email: {user.email}")
        
        # Check for duplicate email
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
            logger.error(f"Database integrity error while creating user: {e}")
            raise DuplicateEmailError(user.email)

    def update_user(self, user_id: UUID, user: models.UserUpdate) -> User:
        """Update an existing user's information.
        
        Args:
            user_id: The UUID of the user to update.
            user: UserUpdate model containing fields to update.
            
        Returns:
            The updated User entity.
            
        Raises:
            UserNotFoundError: If the user does not exist.
        """
        logger.info(f"Attempting to update user with ID: {user_id}")
        
        db_user = self.get_user_by_id(user_id)  # Raises UserNotFoundError if not found

        if user.firstname is not None:
            db_user.firstname = user.firstname
            logger.debug(f"Updated firstname for user {user_id}")
        if user.lastname is not None:
            db_user.lastname = user.lastname
            logger.debug(f"Updated lastname for user {user_id}")
        if user.password is not None:
            db_user.password_hash = get_password_hash(user.password)
            logger.debug(f"Updated password for user {user_id}")

        self._db.commit()
        self._db.refresh(db_user)
        logger.info(f"Successfully updated user with ID: {user_id}")
        return db_user

    def delete_user(self, user_id: UUID) -> None:
        """Delete a user from the database.
        
        Args:
            user_id: The UUID of the user to delete.
            
        Raises:
            UserNotFoundError: If the user does not exist.
        """
        logger.info(f"Attempting to delete user with ID: {user_id}")
        
        user = self.get_user_by_id(user_id)  # Raises UserNotFoundError if not found
        
        self._db.delete(user)
        self._db.commit()
        logger.info(f"Successfully deleted user with ID: {user_id}")

    def get_user_by_id(self, user_id: UUID) -> User:
        """Retrieve a user by ID, raising an exception if not found.
        
        Args:
            user_id: The UUID of the user to retrieve.
            
        Returns:
            The User entity.
            
        Raises:
            UserNotFoundError: If the user does not exist.
        """
        user = self.get_user(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise UserNotFoundError(user_id)
        logger.debug(f"Successfully retrieved user with ID: {user_id}")
        return user

    def change_password(self, user_id: UUID, password_change: models.PasswordChange) -> None:
        """Change a user's password.
        
        Args:
            user_id: The UUID of the user changing their password.
            password_change: PasswordChange model with current and new passwords.
            
        Raises:
            UserNotFoundError: If the user does not exist.
            InvalidPasswordError: If the current password is incorrect.
            PasswordMismatchError: If the new passwords do not match.
        """
        logger.info(f"Password change attempt for user ID: {user_id}")
        
        user = self.get_user_by_id(user_id)

        if not verify_password(password_change.current_password, user.password_hash):
            logger.warning(f"Invalid current password provided for user ID: {user_id}")
            raise InvalidPasswordError()

        if password_change.new_password != password_change.new_password_confirm:
            logger.warning(f"Password mismatch during change attempt for user ID: {user_id}")
            raise PasswordMismatchError()

        user.password_hash = get_password_hash(password_change.new_password)
        self._db.commit()
        logger.info(f"Successfully changed password for user ID: {user_id}")
