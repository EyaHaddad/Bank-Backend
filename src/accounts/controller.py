from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_user
from src.database.core import get_db
from src.entities.user import User
from src.entities.account import Account

router = APIRouter()

@router.post("/beneficiary")
def add_beneficiary(
    name: str,
    bank: str,
    account_number: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = Account(
        user_id=current_user.id,
        beneficiary_name=name,
        bank=bank,
        account_number=account_number,
    )
    db.add(account)
    db.commit()
    return {"message": "Beneficiary added"}
