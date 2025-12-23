"""Transaction router - API endpoints for transaction operations."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.modules.auth.service import get_current_user
from src.infrastructure.database import get_db
from src.models.user import User
from src.models.transaction import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/transfer")
def transfer(
    account_id: int,
    beneficiary_account: str,
    amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Transfer money to a beneficiary."""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    tx = Transaction(
        user_id=current_user.id,
        account_id=account_id,
        beneficiary_account=beneficiary_account,
        amount=amount,
    )
    db.add(tx)
    db.commit()

    return {"message": "Transfer successful"}
