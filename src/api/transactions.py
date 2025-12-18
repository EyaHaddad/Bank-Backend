from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_user
from src.database.core import get_db
from src.entities.user import User
from src.entities.transaction import Transaction

router = APIRouter()

@router.post("/transfer")
def transfer(
    account_id: int,
    beneficiary_account: str,
    amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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
