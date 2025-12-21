"""Account controller module for handling account-related HTTP requests.

This module defines the API endpoints for bank account management operations.
"""
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, status

from src.database.core import DbSession
from . import model
from .service import AccountService
from src.auth.services import CurrentUser

# Configure module-level logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


def get_account_service(db: DbSession) -> AccountService:
    """Provide an account service bound to the current request DB session.
    
    Args:
        db: Database session dependency.
        
    Returns:
        AccountService instance bound to the database session.
    """
    return AccountService(db)


@router.get("/", response_model=list[model.AccountResponse])
def get_my_accounts(
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> list[model.AccountResponse]:
    """Get all accounts for the currently authenticated user.
    
    Args:
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        List of user's accounts.
    """
    logger.debug(f"Fetching accounts for user: {current_user.get_uuid()}")
    return service.list_accounts(current_user.get_uuid())


@router.post("/", response_model=model.AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: model.AccountCreate,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> model.AccountResponse:
    """Create a new bank account for the current user.
    
    Args:
        account_data: Account creation data.
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        The created account's data.
    """
    logger.info(f"Creating new account for user: {current_user.get_uuid()}")
    return service.create_account(current_user.get_uuid(), account_data)


@router.get("/{account_id}", response_model=model.AccountResponse)
def get_account(
    account_id: UUID,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> model.AccountResponse:
    """Get a specific account by ID.
    
    Args:
        account_id: The UUID of the account to retrieve.
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        The account's data.
        
    Raises:
        HTTPException 404: If account not found.
        HTTPException 403: If user doesn't own the account.
    """
    logger.debug(f"Fetching account {account_id} for user: {current_user.get_uuid()}")
    return service.get_user_account(account_id, current_user.get_uuid())


@router.put("/{account_id}", response_model=model.AccountResponse)
def update_account(
    account_id: UUID,
    account_data: model.AccountUpdate,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> model.AccountResponse:
    """Update an account's information.
    
    Args:
        account_id: The UUID of the account to update.
        account_data: Account update data (partial update supported).
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        The updated account's data.
        
    Raises:
        HTTPException 404: If account not found.
        HTTPException 403: If user doesn't own the account.
    """
    logger.info(f"Updating account {account_id} for user: {current_user.get_uuid()}")
    return service.update_account(account_id, current_user.get_uuid(), account_data)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: UUID,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> None:
    """Delete an account.
    
    Args:
        account_id: The UUID of the account to delete.
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Raises:
        HTTPException 404: If account not found.
        HTTPException 403: If user doesn't own the account.
    """
    logger.info(f"Deleting account {account_id} for user: {current_user.get_uuid()}")
    service.delete_account(account_id, current_user.get_uuid())


@router.get("/{account_id}/balance", response_model=model.BalanceResponse)
def get_balance(
    account_id: UUID,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> model.BalanceResponse:
    """Get the balance of an account.
    
    Args:
        account_id: The UUID of the account.
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        The account's balance information.
        
    Raises:
        HTTPException 404: If account not found.
        HTTPException 403: If user doesn't own the account.
    """
    logger.debug(f"Fetching balance for account {account_id}")
    return service.get_balance(account_id, current_user.get_uuid())


@router.post("/{account_id}/deposit", response_model=model.AccountResponse)
def deposit(
    account_id: UUID,
    deposit_data: model.DepositRequest,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> model.AccountResponse:
    """Deposit funds into an account.
    
    Args:
        account_id: The UUID of the account to deposit into.
        deposit_data: Deposit request data.
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        The updated account's data.
        
    Raises:
        HTTPException 404: If account not found.
        HTTPException 403: If user doesn't own the account.
        HTTPException 400: If amount is invalid.
    """
    logger.info(f"Processing deposit to account {account_id}")
    return service.deposit(account_id, current_user.get_uuid(), deposit_data.amount)


@router.post("/{account_id}/withdraw", response_model=model.AccountResponse)
def withdraw(
    account_id: UUID,
    withdraw_data: model.WithdrawRequest,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> model.AccountResponse:
    """Withdraw funds from an account.
    
    Args:
        account_id: The UUID of the account to withdraw from.
        withdraw_data: Withdrawal request data.
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        The updated account's data.
        
    Raises:
        HTTPException 404: If account not found.
        HTTPException 403: If user doesn't own the account.
        HTTPException 400: If amount is invalid or insufficient funds.
    """
    logger.info(f"Processing withdrawal from account {account_id}")
    return service.withdraw(account_id, current_user.get_uuid(), withdraw_data.amount)


@router.post("/{account_id}/transfer", response_model=dict)
def transfer(
    account_id: UUID,
    transfer_data: model.TransferRequest,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> dict:
    """Transfer funds to another account.
    
    Args:
        account_id: The UUID of the source account.
        transfer_data: Transfer request data.
        current_user: The authenticated user from JWT token.
        service: Account service dependency.
        
    Returns:
        Transfer confirmation with updated balances.
        
    Raises:
        HTTPException 404: If either account not found.
        HTTPException 403: If user doesn't own the source account.
        HTTPException 400: If amount is invalid or insufficient funds.
    """
    logger.info(f"Processing transfer from account {account_id} to {transfer_data.target_account_id}")
    source, target = service.transfer(
        account_id, 
        current_user.get_uuid(), 
        transfer_data.target_account_id, 
        transfer_data.amount
    )
    return {
        "message": "Transfer successful",
        "source_account": {
            "id": str(source.id),
            "balance": source.balance,
            "currency": source.currency
        },
        "target_account_id": str(target.id),
        "amount_transferred": transfer_data.amount
    }
