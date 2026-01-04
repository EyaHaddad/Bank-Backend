"""Admin router - API endpoints for admin operations."""

from uuid import UUID
from typing import List

from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from . import schemas
from . import service

from src.infrastructure.database import DbSession
from src.modules.auth.service import AdminUser

router = APIRouter(prefix="/admin", tags=["admin"])


# ==================== USER MANAGEMENT ENDPOINTS ====================

@router.get("/users", response_model=List[schemas.AdminUserResponse], status_code=HTTP_200_OK)
async def list_all_users(
    db: DbSession,
    current_user: AdminUser,
):
    """Get all users in the system. Only accessible by admins."""
    return service.list_all_users(db)


@router.get("/users/{user_id}", response_model=schemas.AdminUserResponse, status_code=HTTP_200_OK)
async def get_user(
    user_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Get a specific user by ID. Only accessible by admins."""
    return service.get_user_by_id(db, user_id)


@router.put("/users/{user_id}", response_model=schemas.AdminUserResponse, status_code=HTTP_200_OK)
async def update_user(
    user_id: UUID,
    user_data: schemas.AdminUserUpdate,
    db: DbSession,
    current_user: AdminUser,
):
    """Update a user's information. Only accessible by admins."""
    return service.admin_update_user(db, user_id, user_data.firstname, user_data.lastname, user_data.email)


@router.post("/users/{user_id}/activate", response_model=schemas.UserStatusResponse, status_code=HTTP_200_OK)
async def activate_user(
    user_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Activate a deactivated user account. Only accessible by admins."""
    user = service.activate_user(db, user_id)
    return schemas.UserStatusResponse(
        message="User activated successfully.",
        user_id=user.id,
        is_active=user.is_active
    )


@router.post("/users/{user_id}/deactivate", response_model=schemas.UserStatusResponse, status_code=HTTP_200_OK)
async def deactivate_user(
    user_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Deactivate a user account. Only accessible by admins."""
    user = service.deactivate_user(db, user_id, current_user.get_uuid())
    return schemas.UserStatusResponse(
        message="User deactivated successfully.",
        user_id=user.id,
        is_active=user.is_active
    )


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Delete a user and all their data. Only accessible by admins."""
    service.admin_delete_user(db, user_id, current_user.get_uuid())


# ==================== ACCOUNT MANAGEMENT ENDPOINTS ====================

@router.get("/accounts", response_model=List[schemas.AdminAccountResponse], status_code=HTTP_200_OK)
async def list_all_accounts(
    db: DbSession,
    current_user: AdminUser,
):
    """Get all accounts in the system. Only accessible by admins."""
    return service.list_all_accounts(db)


@router.post("/accounts", response_model=schemas.AdminAccountResponse, status_code=HTTP_200_OK)
async def create_account_for_user(
    account_data: schemas.AdminAccountCreate,
    db: DbSession,
    current_user: AdminUser,
):
    """Create a new account for a specific user. Only accessible by admins."""
    return service.create_account_for_user(db, account_data)


@router.post("/accounts/{account_id}/activate", response_model=schemas.AccountStatusResponse, status_code=HTTP_200_OK)
async def activate_account(
    account_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Activate a blocked account. Only accessible by admins."""
    account = service.activate_account(db, account_id)
    return schemas.AccountStatusResponse(
        message="Account activated successfully.",
        account_id=account.id,
        status=account.status.value
    )


@router.post("/accounts/{account_id}/block", response_model=schemas.AccountStatusResponse, status_code=HTTP_200_OK)
async def block_account(
    account_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Block an account. Only accessible by admins."""
    account = service.block_account(db, account_id)
    return schemas.AccountStatusResponse(
        message="Account blocked successfully.",
        account_id=account.id,
        status=account.status.value
    )


@router.post("/accounts/{account_id}/close", response_model=schemas.AccountStatusResponse, status_code=HTTP_200_OK)
async def close_account(
    account_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Close an account permanently. Only accessible by admins."""
    account = service.close_account(db, account_id)
    return schemas.AccountStatusResponse(
        message="Account closed successfully.",
        account_id=account.id,
        status=account.status.value
    )


@router.delete("/accounts/{account_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Delete an account permanently. Only accessible by admins."""
    service.delete_account(db, account_id)


@router.put("/accounts/{account_id}/balance", response_model=schemas.AdminAccountResponse, status_code=HTTP_200_OK)
async def update_account_balance(
    account_id: UUID,
    balance_data: schemas.AccountBalanceUpdate,
    db: DbSession,
    current_user: AdminUser,
):
    """Update account balance (admin correction). Only accessible by admins."""
    account = service.update_account_balance(db, account_id, balance_data.new_balance)
    user = service.get_user_by_id(db, account.user_id)
    return schemas.AdminAccountResponse(
        id=account.id,
        user_id=account.user_id,
        user_name=f"{user.firstname} {user.lastname}",
        user_email=user.email,
        balance=account.balance,
        currency=account.currency,
        status=account.status.value
    )


# ==================== ROLE MANAGEMENT ENDPOINTS ====================

@router.post("/promote/{user_id}", response_model=schemas.PromoteUserResponse, status_code=HTTP_200_OK)
async def promote_user_to_admin(
    user_id: UUID,
    db: DbSession,
    current_user: AdminUser,
):
    """Promote a user to admin role. Only accessible by admins."""
    user = service.promote_user_to_admin(db, user_id)
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
    user = service.demote_admin_to_user(db, user_id, current_user.get_uuid())
    return schemas.PromoteUserResponse(
        message="Admin demoted to user successfully.",
        user_id=user.id,
        new_role=user.role.value
    )
