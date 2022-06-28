from typing import List, Optional
from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.Transaction, db:Session = Depends(get_db)):
    new_transaction = models.Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.put("/{id}", response_model=schemas.Transaction)
def update_transaction(id: int, updated_transaction: schemas.Transaction, db: Session = Depends(get_db)):
    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)
    transaction = transaction_query.first()

    if transaction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction with id {id} does not exist.")

    transaction_query.update(updated_transaction.dict(), synchronize_session=False)

    db.commit()

    return transaction_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(id: int, db: Session = Depends(get_db)):
    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)
    transaction = transaction_query.first()

    if transaction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction with id {id} does not exist.")

    transaction_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", response_model=List[schemas.Transaction])
def get_transactions(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    transactions = db.query(models.Transaction).filter(models.Transaction.description.contains(search)).limit(limit).offset(skip).all()
    return transactions

@router.get("/{id}", response_model=schemas.Transaction)
def get_transaction(id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == id).first()

    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction with id {id} does not exist.")

    return transaction


