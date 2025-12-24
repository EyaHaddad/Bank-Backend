"""Transaction router - API endpoints for transaction operations."""

import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.modules.auth.service import CurrentUser
from src.infrastructure.database import DbSession
from src.models.transaction import TransactionType, TransactionStatus
from src.modules.notifications.service import send_transaction_notification_helper

from . import schemas
from .service import TransactionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_transaction_service(db: DbSession) -> TransactionService:
    """Provide a transaction service bound to the current request DB session."""
    return TransactionService(db)


@router.post("/credit", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def credit_account(
    request: schemas.CreditRequest,
    current_user: CurrentUser,
    db: DbSession,
    service: TransactionService = Depends(get_transaction_service),
) -> schemas.TransactionResponse:
    """
    Credit (deposit) money to an account.
    
    This endpoint allows the authenticated user to deposit money into their account.
    """
    logger.info(f"User {current_user.user_id} requesting credit to account {request.account_id}")
    transaction = service.credit(current_user.get_uuid(), request)
    
    # Send notification
    try:
        send_transaction_notification_helper(
            db=db,
            user_id=current_user.get_uuid(),
            transaction_type="credit",
            amount=request.amount,
            reference=transaction.reference,
        )
    except Exception as e:
        logger.warning(f"Failed to send transaction notification: {str(e)}")
    
    return transaction


@router.post("/debit", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def debit_account(
    request: schemas.DebitRequest,
    current_user: CurrentUser,
    db: DbSession,
    service: TransactionService = Depends(get_transaction_service),
) -> schemas.TransactionResponse:
    """
    Debit (withdraw) money from an account.
    
    This endpoint allows the authenticated user to withdraw money from their account.
    """
    logger.info(f"User {current_user.user_id} requesting debit from account {request.account_id}")
    transaction = service.debit(current_user.get_uuid(), request)
    
    # Send notification
    try:
        send_transaction_notification_helper(
            db=db,
            user_id=current_user.get_uuid(),
            transaction_type="debit",
            amount=request.amount,
            reference=transaction.reference,
        )
    except Exception as e:
        logger.warning(f"Failed to send transaction notification: {str(e)}")
    
    return transaction


@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: UUID,
    current_user: CurrentUser,
    service: TransactionService = Depends(get_transaction_service),
) -> schemas.TransactionResponse:
    """
    Get a specific transaction by ID.
    
    The user must own the account associated with the transaction.
    """
    logger.debug(f"User {current_user.user_id} fetching transaction {transaction_id}")
    return service.get_user_transaction(transaction_id, current_user.get_uuid())


@router.get("/account/{account_id}", response_model=schemas.TransactionListResponse)
def list_account_transactions(
    account_id: UUID,
    current_user: CurrentUser,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    transaction_type: Optional[str] = Query(None, description="Filter by transaction type (CREDIT, DEBIT, TRANSFER)"),
    transaction_status: Optional[str] = Query(None, description="Filter by status (PENDING, COMPLETED, FAILED)"),
    service: TransactionService = Depends(get_transaction_service),
) -> schemas.TransactionListResponse:
    """
    List all transactions for a specific account with pagination and optional filters.
    
    The user must own the account to view its transactions.
    """
    logger.debug(f"User {current_user.user_id} listing transactions for account {account_id}")
    
    # Convert string filters to enums if provided
    type_filter = TransactionType(transaction_type) if transaction_type else None
    status_filter = TransactionStatus(transaction_status) if transaction_status else None
    
    return service.list_transactions_by_account(
        account_id=account_id,
        user_id=current_user.get_uuid(),
        page=page,
        page_size=page_size,
        transaction_type=type_filter,
        status=status_filter,
    )


@router.get("/", response_model=schemas.TransactionListResponse)
def list_my_transactions(
    current_user: CurrentUser,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    transaction_type: Optional[str] = Query(None, description="Filter by transaction type (CREDIT, DEBIT, TRANSFER)"),
    transaction_status: Optional[str] = Query(None, description="Filter by status (PENDING, COMPLETED, FAILED)"),
    service: TransactionService = Depends(get_transaction_service),
) -> schemas.TransactionListResponse:
    """
    List all transactions for the current user across all their accounts.
    
    Supports pagination and optional filters.
    """
    logger.debug(f"User {current_user.user_id} listing all their transactions")
    
    # Convert string filters to enums if provided
    type_filter = TransactionType(transaction_type) if transaction_type else None
    status_filter = TransactionStatus(transaction_status) if transaction_status else None
    
    return service.list_user_transactions(
        user_id=current_user.get_uuid(),
        page=page,
        page_size=page_size,
        transaction_type=type_filter,
        status=status_filter,
    )


@router.get("/account/{account_id}/summary", response_model=schemas.TransactionSummary)
def get_account_summary(
    account_id: UUID,
    current_user: CurrentUser,
    start_date: Optional[datetime] = Query(None, description="Start date for summary period"),
    end_date: Optional[datetime] = Query(None, description="End date for summary period"),
    service: TransactionService = Depends(get_transaction_service),
) -> schemas.TransactionSummary:
    """
    Get transaction summary/statistics for a specific account.
    
    Optionally filter by date range.
    """
    logger.debug(f"User {current_user.user_id} getting summary for account {account_id}")
    return service.get_transaction_summary(
        account_id=account_id,
        user_id=current_user.get_uuid(),
        start_date=start_date,
        end_date=end_date,
    )



