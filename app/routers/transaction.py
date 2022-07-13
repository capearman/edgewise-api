from typing import List, Optional
from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.TransactionCreateOut)
def create_transaction(transaction: schemas.TransactionCreateIn, db:Session = Depends(get_db)):
    new_transaction = models.Transaction(**transaction.dict())
    
    category_id_query = db.query(models.Category.id).filter(models.Category.name == new_transaction.category)
    category_id = category_id_query.first()

    if not category_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with name {new_transaction.category} does not exist")

    new_transaction.category_id = category_id[0]

    category_type_query = db.query(models.Category.type).filter(models.Category.id == new_transaction.category_id)
    category_type = category_type_query.first()

    if category_type[0] != new_transaction.type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction type (Income or Expense) must match category")

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.put("/{id}", response_model=schemas.TransactionReadOnly)
def update_transaction(id: int, updated_transaction: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)
    transaction = transaction_query.first()

    if transaction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction with id {id} does not exist.")

    category_query = db.query(models.Category.name).filter(models.Category.name == updated_transaction.category)
    category = category_query.first()

    updated_transaction_category_id = db.query(models.Category.id).filter(models.Category.name == updated_transaction.category).first()

    if category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with name {updated_transaction.category} does not exist.")

    category_type_query = db.query(models.Category.type).filter(models.Category.id == updated_transaction_category_id[0])
    category_type = category_type_query.first()

    if category_type[0] != updated_transaction.type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction type (Income or Expense) must match category")

    transaction_query.update(updated_transaction.dict(), synchronize_session=False)

    db.commit()

    def category_id_update(query, category_name: str, category_id: int):
        transaction = query.first()
        transaction.category_name = category_name
        transaction.category_id = category_id[0]

        new_transaction = schemas.TransactionReadOnly(id = transaction.id, type=transaction.type, date=transaction.date, amount=transaction.amount, description=transaction.description, category=transaction.category, category_id=transaction.category_id, check_box=transaction.check_box)

        query.update(new_transaction.dict(), synchronize_session=False)
        db.commit()

    category_id_update(transaction_query, updated_transaction.category, updated_transaction_category_id)

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


