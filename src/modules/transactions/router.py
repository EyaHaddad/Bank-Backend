"""Transaction router - API endpoints for transaction operations."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.modules.auth.service import CurrentUser
from src.infrastructure.database import get_db
from src.models.transaction import Transaction
from src.models.account import Account
from src.modules.notifications.service import send_transaction_notification_helper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/transfer")
def transfer(
    account_id: int,
    beneficiary_account: str,
    amount: float,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Transfer money to a beneficiary."""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    tx = Transaction(
        user_id=UUID(current_user.user_id),
        account_id=account_id,
        beneficiary_account=beneficiary_account,
        amount=amount,
    )
    db.add(tx)
    db.commit()

    # Send transaction notification to the user
    try:
        user_id = UUID(current_user.user_id)
        
        send_transaction_notification_helper(
            db=db,
            user_id=user_id,
            transaction_type="debit",  # Transfer is a debit from sender's account
            amount=amount,
            account_number=str(account_id),
            reference=f"Transfer to {beneficiary_account}",
        )
        logger.info(f"Transaction notification sent for transfer of {amount}")
    except Exception as e:
        logger.error(f"Failed to send transaction notification: {str(e)}")

    return {"message": "Transfer successful"}
