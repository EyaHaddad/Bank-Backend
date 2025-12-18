"User services module for user-related operations."
"all the business logic related to users : the CRUD"
from uuid import UUID

from sqlalchemy.orm import Session

from . import models
from src.entities.user import User
from src.auth.exceptions import InvalidPasswordError, PasswordMismatchError, UserNotFoundError
from src.auth.services import get_password_hash, verify_password
import logging


class UserService:
    def __init__(self, session: Session):
        """The service receives a database session."""
        self._db = session

    def list_users(self) -> list[User]:
        return self._db.query(User).all()

    def get_user(self, user_id: UUID) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: models.UserCreate) -> User:
        new_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password_hash=get_password_hash(user.password),
        )
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return new_user

    def update_user(self, user_id: UUID, user: models.UserUpdate) -> User | None:
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        if user.firstname is not None:
            db_user.firstname = user.firstname
        if user.lastname is not None:
            db_user.lastname = user.lastname
        if user.password is not None:
            db_user.password_hash = get_password_hash(user.password)

        self._db.commit()
        self._db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: UUID) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True

    def get_user_by_id(self, user_id: UUID) -> User:
        user = self.get_user(user_id)
        if not user:
            logging.warning(f"User not found with ID: {user_id}")
            raise UserNotFoundError(user_id)
        logging.info(f"Successfully retrieved user with ID: {user_id}")
        return user

    def change_password(self, user_id: UUID, password_change: models.PasswordChange) -> None:
        user = self.get_user_by_id(user_id)

        if not verify_password(password_change.current_password, user.password_hash):
            logging.warning(f"Invalid current password provided for user ID: {user_id}")
            raise InvalidPasswordError()

        if password_change.new_password != password_change.new_password_confirm:
            logging.warning(f"Password mismatch during change attempt for user ID: {user_id}")
            raise PasswordMismatchError()

        user.password_hash = get_password_hash(password_change.new_password)
        self._db.commit()
        logging.info(f"Successfully changed password for user ID: {user_id}")
