from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_transactions(transaction: schemas.Transaction, db:Session = Depends(get_db)):
    new_transaction = models.Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

