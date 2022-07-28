from typing import List, Optional
from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, category_class, header_class, oauth2

router = APIRouter(
    prefix="/last_month_balance",
    tags=['Last Month Balance']
)

@router.get("/", response_model=schemas.LastMonthBalance)
def get_last_month_balance(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    balance = db.query(models.User.last_month_balance).filter(models.User.id == current_user.id).first()

    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist")

    return balance


@router.put("/", response_model=schemas.LastMonthBalance)
def update_last_month_balance(updated_balance: schemas.LastMonthBalance, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    balance = db.query(models.User.last_month_balance).filter(models.User.id == current_user.id).first()


    balance_update_query = db.query(models.User).filter(models.User.id == current_user.id)

    if balance == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist.")

    balance_update_query.update(updated_balance.dict(), synchronize_session=False)
    db.commit()
    new_balance = db.query(models.User.last_month_balance).filter(models.User.id == current_user.id).first()
    return new_balance

