"""Admin Services."""

import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.models.user import User, Role
from src.modules.auth.schemas import TokenData
from .exceptions import UserNotFoundError, UserAlreadyAdminError


def promote_user_to_admin(db: Session, user_id: UUID, current_user: TokenData) -> User:
    """Promote a user to admin role. Only admins can perform this action."""
    # Find the target user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(str(user_id))
    
    # Check if already admin
    if user.role == Role.ADMIN:
        raise UserAlreadyAdminError(str(user_id))
    
    # Promote to admin
    user.role = Role.ADMIN
    db.commit()
    db.refresh(user)
    
    logging.info(f"User {user_id} promoted to admin by {current_user.user_id}")
    return user


def demote_admin_to_user(db: Session, user_id: UUID, current_user: TokenData) -> User:
    """Demote an admin to regular user role. Only admins can perform this action."""
    # Cannot demote yourself
    if str(user_id) == current_user.user_id:
        from fastapi import HTTPException
        from starlette.status import HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Cannot demote yourself."
        )
    
    # Find the target user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(str(user_id))
    
    # Check if already regular user
    if user.role == Role.USER:
        from fastapi import HTTPException
        from starlette.status import HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} is already a regular user."
        )
    
    # Demote to user
    user.role = Role.USER
    db.commit()
    db.refresh(user)
    
    logging.info(f"Admin {user_id} demoted to user by {current_user.user_id}")
    return user
