"""Admin Services - Orchestrates admin operations using other module services."""

import logging
from uuid import UUID
from typing import List

from sqlalchemy.orm import Session

from src.models.user import User
from src.models.account import Account
from src.modules.users.service import UserService
from src.modules.accounts.service import AccountService
from .schemas import AdminAccountResponse

logger = logging.getLogger(__name__)


# ==================== HELPER FUNCTIONS ====================

def get_user_service(db: Session) -> UserService:
    """Get an instance of UserService."""
    return UserService(db)


def get_account_service(db: Session) -> AccountService:
    """Get an instance of AccountService."""
    return AccountService(db)


# ==================== USER MANAGEMENT (delegated to UserService) ====================

def list_all_users(db: Session) -> List[User]:
    """Get all users in the system."""
    return get_user_service(db).list_users()


def get_user_by_id(db: Session, user_id: UUID) -> User:
    """Get a user by ID."""
    return get_user_service(db).get_user_by_id(user_id)


def activate_user(db: Session, user_id: UUID) -> User:
    """Activate a user account."""
    user = get_user_service(db).activate_user(user_id)
    logger.info(f"Admin activated user {user_id}")
    return user


def deactivate_user(db: Session, user_id: UUID, current_user_id: UUID) -> User:
    """Deactivate a user account."""
    user = get_user_service(db).deactivate_user(user_id, current_user_id)
    logger.info(f"Admin deactivated user {user_id}")
    return user


def admin_delete_user(db: Session, user_id: UUID, current_user_id: UUID) -> bool:
    """Delete a user and all their accounts."""
    result = get_user_service(db).admin_delete_user(user_id, current_user_id)
    logger.info(f"Admin deleted user {user_id}")
    return result


def admin_update_user(db: Session, user_id: UUID, firstname: str = None, lastname: str = None, email: str = None) -> User:
    """Update a user's information (admin only)."""
    return get_user_service(db).admin_update_user(user_id, firstname, lastname, email)


def promote_user_to_admin(db: Session, user_id: UUID) -> User:
    """Promote a user to admin role."""
    user = get_user_service(db).promote_to_admin(user_id)
    logger.info(f"User {user_id} promoted to admin")
    return user


def demote_admin_to_user(db: Session, user_id: UUID, current_user_id: UUID) -> User:
    """Demote an admin to regular user role."""
    user = get_user_service(db).demote_to_user(user_id, current_user_id)
    logger.info(f"Admin {user_id} demoted to user")
    return user


# ==================== ACCOUNT MANAGEMENT (delegated to AccountService) ====================

def list_all_accounts(db: Session) -> List[AdminAccountResponse]:
    """Get all accounts in the system with user information."""
    service = get_account_service(db)
    user_service = get_user_service(db)
    accounts = service.list_all_accounts()
    
    result = []
    for account in accounts:
        user = user_service.get_user(account.user_id)
        result.append(AdminAccountResponse(
            id=account.id,
            user_id=account.user_id,
            user_name=f"{user.firstname} {user.lastname}" if user else "Unknown",
            user_email=user.email if user else "Unknown",
            balance=account.balance,
            currency=account.currency,
            status=account.status.value if account.status else "ACTIVE"
        ))
    
    return result


def get_account_by_id(db: Session, account_id: UUID) -> Account:
    """Get an account by ID."""
    return get_account_service(db).get_account_by_id(account_id)


def activate_account(db: Session, account_id: UUID) -> Account:
    """Activate a blocked account."""
    account = get_account_service(db).activate_account(account_id)
    logger.info(f"Admin activated account {account_id}")
    return account


def block_account(db: Session, account_id: UUID) -> Account:
    """Block an account."""
    account = get_account_service(db).block_account(account_id)
    logger.info(f"Admin blocked account {account_id}")
    return account


def close_account(db: Session, account_id: UUID) -> Account:
    """Close an account permanently."""
    account = get_account_service(db).close_account(account_id)
    logger.info(f"Admin closed account {account_id}")
    return account


def delete_account(db: Session, account_id: UUID) -> bool:
    """Delete an account permanently."""
    result = get_account_service(db).admin_delete_account(account_id)
    logger.info(f"Admin deleted account {account_id}")
    return result


def update_account_balance(db: Session, account_id: UUID, new_balance: float) -> Account:
    """Update account balance (admin only - for corrections)."""
    account = get_account_service(db).update_balance(account_id, new_balance)
    logger.info(f"Admin updated account {account_id} balance to {new_balance}")
    return account
