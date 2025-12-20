"""User controller module for handling user-related HTTP requests.

This module defines the API endpoints for user management operations.
"""
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, status

from src.database.core import DbSession
from . import models
from .service import UserService
from ..auth.services import CurrentUser

# Configure module-level logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: DbSession) -> UserService:
    """Provide a user service bound to the current request DB session.
    
    Args:
        db: Database session dependency.
        
    Returns:
        UserService instance bound to the database session.
    """
    return UserService(db)


@router.get("/me", response_model=models.UserResponseModel)
def get_current_user(
    current_user: CurrentUser,
    service: UserService = Depends(get_user_service)
) -> models.UserResponseModel:
    """Get the currently authenticated user's profile.
    
    Args:
        current_user: The authenticated user from JWT token.
        service: User service dependency.
        
    Returns:
        The current user's profile data.
        
    Raises:
        HTTPException 404: If user not found (should not happen for authenticated users).
    """
    logger.debug(f"Fetching profile for current user: {current_user.get_uuid()}")
    return service.get_user_by_id(current_user.get_uuid())


@router.get("/", response_model=list[models.UserResponseModel])
def get_users(
    service: UserService = Depends(get_user_service)
) -> list[models.UserResponseModel]:
    """Get all users in the system.
    
    Args:
        service: User service dependency.
        
    Returns:
        List of all users.
    """
    logger.debug("Fetching all users")
    return service.list_users()


@router.post("/", response_model=models.UserResponseModel, status_code=status.HTTP_201_CREATED)
def create_user(
    user: models.UserCreate,
    service: UserService = Depends(get_user_service)
) -> models.UserResponseModel:
    """Create a new user.
    
    Args:
        user: User creation data.
        service: User service dependency.
        
    Returns:
        The created user's profile data.
        
    Raises:
        HTTPException 409: If email already exists.
    """
    logger.info(f"Creating new user with email: {user.email}")
    return service.create_user(user)


@router.get("/{user_id}", response_model=models.UserResponseModel)
def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service)
) -> models.UserResponseModel:
    """Get a specific user by ID.
    
    Args:
        user_id: The UUID of the user to retrieve.
        service: User service dependency.
        
    Returns:
        The user's profile data.
        
    Raises:
        HTTPException 404: If user not found.
    """
    logger.debug(f"Fetching user with ID: {user_id}")
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=models.UserResponseModel)
def update_user(
    user_id: UUID,
    user: models.UserUpdate,
    service: UserService = Depends(get_user_service)
) -> models.UserResponseModel:
    """Update a user's information.
    
    Args:
        user_id: The UUID of the user to update.
        user: User update data (partial update supported).
        service: User service dependency.
        
    Returns:
        The updated user's profile data.
        
    Raises:
        HTTPException 404: If user not found.
    """
    logger.info(f"Updating user with ID: {user_id}")
    return service.update_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service)
) -> None:
    """Delete a user.
    
    Args:
        user_id: The UUID of the user to delete.
        service: User service dependency.
        
    Raises:
        HTTPException 404: If user not found.
    """
    logger.info(f"Deleting user with ID: {user_id}")
    service.delete_user(user_id)


@router.post("/me/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_change: models.PasswordChange,
    current_user: CurrentUser,
    service: UserService = Depends(get_user_service),
) -> dict:
    """Change the current user's password.
    
    Args:
        password_change: Password change data with current and new passwords.
        current_user: The authenticated user from JWT token.
        service: User service dependency.
        
    Returns:
        Success confirmation message.
        
    Raises:
        HTTPException 401: If current password is incorrect.
        HTTPException 400: If new passwords do not match.
    """
    logger.info(f"Password change request for user: {current_user.get_uuid()}")
    service.change_password(current_user.get_uuid(), password_change)
    return {"message": "Password changed successfully"}
