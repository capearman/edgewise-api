from typing import List, Optional
from fastapi import APIRouter, status, Response, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, category_class
import json


router = APIRouter(
    prefix="/categories",
    tags=['Categories']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(category:schemas.CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(**category.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/names/{type}", response_model=List[schemas.CategoryName])
def get_category_names(db: Session = Depends(get_db)):
    category_names = db.query(models.Category.name).filter(models.Category.type == type).all()
    return category_names

@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()

    for category in categories:
        actual_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.category == category.name).first()

        actual = actual_query[0]

        if not actual:
            actual = 0

        category_obj = category_class.Category(category.name, category.planned, actual, category.goal)

        setattr(category, 'actual', category_obj.get_actual())
        setattr(category, 'diff', category_obj.get_diff())
        setattr(category, 'goal_met', category_obj.get_goal_met())

    return categories

@router.get("/{id}", response_model=schemas.CategoryOut)
def get_category(id: int, db:Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {id} does not exist")

    actual_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.category == category.name).first()

    actual = actual_query[0]

    category_obj = category_class.Category(category.name, category.planned, actual, category.goal)

    setattr(category, 'actual', category_obj.get_actual())
    setattr(category, 'diff', category_obj.get_diff())
    setattr(category, 'goal_met', category_obj.get_goal_met())

    return category

#TODO: Link Category name with transaction category in database migration
@router.put("/{id}", response_model=schemas.CategoryOut)
def update_category(id: int, updated_category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category_query = db.query(models.Category).filter(models.Category.id == id)

    category = category_query.first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id: {id} does not exist")

    category_query.update(updated_category.dict(), synchronize_session=False)
    db.commit()

    new_updated_category = category_query.first()

    actual_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.category == category.name).first()

    actual = actual_query[0]

    category_obj = category_class.Category(new_updated_category.name, new_updated_category.planned, actual, new_updated_category.goal)

    setattr(new_updated_category, 'actual', category_obj.get_actual())
    setattr(new_updated_category, 'diff', category_obj.get_diff())
    setattr(new_updated_category, 'goal_met', category_obj.get_goal_met())

    return new_updated_category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):
    category_query = db.query(models.Category).filter(models.Category.id == id)

    category = category_query.first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id: {id} does not exist")

    category_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





