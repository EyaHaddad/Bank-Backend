"""Account router - API endpoints for account operations."""

from uuid import UUID
import logging

from fastapi import APIRouter, Depends, status

from src.infrastructure.database import DbSession
from . import schemas
from .service import AccountService
from src.modules.auth import CurrentUser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


def get_account_service(db: DbSession) -> AccountService:
    """Provide an account service bound to the current request DB session."""
    return AccountService(db)


@router.get("/", response_model=list[schemas.AccountResponse])
def get_my_accounts(
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> list[schemas.AccountResponse]:
    """Get all accounts for the currently authenticated user."""
    logger.debug(f"Fetching accounts for user: {current_user.get_uuid()}")
    return service.list_accounts(current_user.get_uuid())


@router.post("/", response_model=schemas.AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: schemas.AccountCreate,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> schemas.AccountResponse:
    """Create a new bank account for the current user."""
    logger.info(f"Creating new account for user: {current_user.get_uuid()}")
    return service.create_account(current_user.get_uuid(), account_data)


@router.get("/{account_id}", response_model=schemas.AccountResponse)
def get_account(
    account_id: UUID,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> schemas.AccountResponse:
    """Get a specific account by ID."""
    logger.debug(f"Fetching account {account_id} for user: {current_user.get_uuid()}")
    return service.get_user_account(account_id, current_user.get_uuid())


@router.put("/{account_id}", response_model=schemas.AccountResponse)
def update_account(
    account_id: UUID,
    account_data: schemas.AccountUpdate,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> schemas.AccountResponse:
    """Update an account."""
    logger.info(f"Updating account {account_id} for user: {current_user.get_uuid()}")
    return service.update_account(account_id, current_user.get_uuid(), account_data)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: UUID,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
):
    """Delete an account."""
    logger.info(f"Deleting account {account_id} for user: {current_user.get_uuid()}")
    service.delete_account(account_id, current_user.get_uuid())


@router.post("/{account_id}/deposit", response_model=schemas.AccountResponse)
def deposit(
    account_id: UUID,
    deposit_data: schemas.DepositRequest,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> schemas.AccountResponse:
    """Deposit money into an account."""
    logger.info(f"Depositing {deposit_data.amount} to account {account_id}")
    return service.deposit(account_id, current_user.get_uuid(), deposit_data.amount)


@router.post("/{account_id}/withdraw", response_model=schemas.AccountResponse)
def withdraw(
    account_id: UUID,
    withdraw_data: schemas.WithdrawRequest,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> schemas.AccountResponse:
    """Withdraw money from an account."""
    logger.info(f"Withdrawing {withdraw_data.amount} from account {account_id}")
    return service.withdraw(account_id, current_user.get_uuid(), withdraw_data.amount)


@router.post("/{account_id}/transfer", response_model=schemas.AccountResponse)
def transfer(
    account_id: UUID,
    transfer_data: schemas.TransferRequest,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> schemas.AccountResponse:
    """Transfer money between accounts."""
    logger.info(f"Transferring {transfer_data.amount} from account {account_id} to {transfer_data.target_account_id}")
    return service.transfer(account_id, current_user.get_uuid(), transfer_data.target_account_id, transfer_data.amount)


@router.get("/{account_id}/balance", response_model=schemas.BalanceResponse)
def get_balance(
    account_id: UUID,
    current_user: CurrentUser,
    service: AccountService = Depends(get_account_service)
) -> schemas.BalanceResponse:
    """Get the balance of an account."""
    logger.debug(f"Fetching balance for account {account_id}")
    return service.get_balance(account_id, current_user.get_uuid())
