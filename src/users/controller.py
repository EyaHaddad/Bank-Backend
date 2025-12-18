from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.database.core import DbSession
from . import models
from .service import UserService
from ..auth.services import CurrentUser

router = APIRouter()


def get_user_service(db: DbSession) -> UserService:
    """Provide a user service bound to the current request DB session."""
    return UserService(db)


@router.get("/me", response_model=models.UserResponseModel)
def get_current_user(current_user: CurrentUser, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(current_user.get_uuid())


@router.get("/", response_model=list[models.UserResponseModel])
def get_users(service: UserService = Depends(get_user_service)):
    return service.list_users()


@router.post("/", response_model=models.UserResponseModel, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)


@router.get("/{user_id}", response_model=models.UserResponseModel)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=models.UserResponseModel)
def update_user(user_id: UUID, user: models.UserUpdate, service: UserService = Depends(get_user_service)):
    updated = service.update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_change: models.PasswordChange,
    current_user: CurrentUser,
    service: UserService = Depends(get_user_service),
):
    service.change_password(current_user.get_uuid(), password_change)
    return {"success": True}
