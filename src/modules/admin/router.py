"""Admin router - API endpoints for admin operations."""

from uuid import UUID

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from . import schemas
from . import service

from src.infrastructure.database import DbSession
from src.modules.auth.service import AdminUser

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/promote/{user_id}", response_model=schemas.PromoteUserResponse, status_code=HTTP_200_OK)
async def promote_user_to_admin(
    user_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Promote a user to admin role. Only accessible by admins."""
    user = service.promote_user_to_admin(db, user_id, current_user)
    return schemas.PromoteUserResponse(
        message="User promoted to admin successfully.",
        user_id=user.id,
        new_role=user.role.value
    )


@router.post("/demote/{user_id}", response_model=schemas.PromoteUserResponse, status_code=HTTP_200_OK)
async def demote_admin_to_user(
    user_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Demote an admin to regular user. Only accessible by admins."""
    user = service.demote_admin_to_user(db, user_id, current_user)
    return schemas.PromoteUserResponse(
        message="Admin demoted to user successfully.",
        user_id=user.id,
        new_role=user.role.value
    )
