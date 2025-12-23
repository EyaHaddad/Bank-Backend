"""User router - API endpoints for user operations."""

from uuid import UUID
import logging

from fastapi import APIRouter, Depends, status

from src.infrastructure.database import DbSession
from . import schemas
from .service import UserService
from src.modules.auth import CurrentUser, AdminUser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: DbSession) -> UserService:
    """Provide a user service bound to the current request DB session."""
    return UserService(db)


@router.get("/me", response_model=schemas.UserResponseModel)
def get_current_user(
    current_user: CurrentUser,
    service: UserService = Depends(get_user_service)
) -> schemas.UserResponseModel:
    """Get the currently authenticated user's profile."""
    logger.debug(f"Fetching profile for current user: {current_user.get_uuid()}")
    return service.get_user_by_id(current_user.get_uuid())


@router.get("/", response_model=list[schemas.UserResponseModel])
def get_users(
    current_user: AdminUser,
    service: UserService = Depends(get_user_service)
) -> list[schemas.UserResponseModel]:
    """Get all users in the system. Admin only."""
    logger.debug("Fetching all users")
    return service.list_users()


@router.post("/", response_model=schemas.UserResponseModel, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    current_user: AdminUser,
    service: UserService = Depends(get_user_service)
) -> schemas.UserResponseModel:
    """Create a new user. Admin only."""
    logger.info(f"Creating new user with email: {user.email}")
    return service.create_user(user)


@router.get("/{user_id}", response_model=schemas.UserResponseModel)
def get_user(
    user_id: UUID,
    current_user: AdminUser,
    service: UserService = Depends(get_user_service)
) -> schemas.UserResponseModel:
    """Get a specific user by ID. Admin only."""
    logger.debug(f"Fetching user with ID: {user_id}")
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=schemas.UserResponseModel)
def update_user(
    user_id: UUID,
    user_data: schemas.UserUpdate,
    current_user: CurrentUser,
    service: UserService = Depends(get_user_service)
) -> schemas.UserResponseModel:
    """Update a user's profile. Users can only update their own profile."""
    # Users can only update their own profile unless they're admin
    if str(user_id) != current_user.user_id and not current_user.is_admin():
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="You can only update your own profile")
    logger.info(f"Updating user with ID: {user_id}")
    return service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    current_user: AdminUser,
    service: UserService = Depends(get_user_service)
):
    """Delete a user. Admin only."""
    logger.info(f"Deleting user with ID: {user_id}")
    service.delete_user(user_id)


@router.post("/{user_id}/change-password", status_code=status.HTTP_200_OK)
def change_password(
    user_id: UUID,
    password_data: schemas.PasswordChange,
    current_user: CurrentUser,
    service: UserService = Depends(get_user_service)
):
    """Change a user's password. Users can only change their own password."""
    # Users can only change their own password
    if str(user_id) != current_user.user_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="You can only change your own password")
    logger.info(f"Changing password for user with ID: {user_id}")
    service.change_password(user_id, password_data)
    return {"message": "Password changed successfully"}
