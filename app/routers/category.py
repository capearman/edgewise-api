from typing import List, Optional
from fastapi import APIRouter, status, Response, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, category_class, exceptions, oauth2
import json


router = APIRouter(
    prefix="/categories",
    tags=['Categories']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryIn)
def create_category(category:schemas.CategoryIn, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_category = models.Category(owner_id = current_user.id, **category.dict())
    
    def pass_to_db(new_category):
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    if category.header == "":
        if new_category.type == 'Expense':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A category without a header cannot be assigned the type 'Expense'")

        return pass_to_db(new_category)
    else:
        if new_category.type == 'Income':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A category with a header cannot be assigned the type 'Income'.")
    
        header_id_query = db.query(models.Header.id).filter(models.Header.name == new_category.header, models.Header.owner_id == current_user.id)
        header_id = header_id_query.first()

        if header_id == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"header with name {new_category.header} does not exist")

        new_category.header_id = header_id[0]

        return pass_to_db(new_category)


@router.get("/names/{type}", response_model=List[schemas.CategoryName])
def get_category_names(type: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if type != "Income" and type != "Expense":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no type: {type}. The only types allowed are 'Income' and Expense'.")
    category_names = db.query(models.Category.name).filter(models.Category.type == type, models.Category.owner_id == current_user.id).all()
    return category_names

@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    categories = db.query(models.Category).filter(models.Category.owner_id == current_user.id).all()

    for category in categories:
        actual_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.category == category.name, models.Transaction.owner_id == current_user.id).first()

        actual = actual_query[0]

        if not actual:
            actual = 0

        category_obj = category_class.Category(category.name, category.planned, actual, category.goal)

        setattr(category, 'actual', category_obj.get_actual())
        setattr(category, 'diff', category_obj.get_diff())
        setattr(category, 'goal_met', category_obj.get_goal_met())

    return categories

@router.get("/{id}", response_model=schemas.CategoryOut)
def get_category(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == id, models.Category.owner_id == current_user.id).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {id} does not exist")

    actual_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.category == category.name, models.Transaction.owner_id == current_user.id).first()

    actual = actual_query[0]

    if actual == None:
        actual = 0

    category_obj = category_class.Category(category.name, category.planned, actual, category.goal)

    setattr(category, 'actual', category_obj.get_actual())
    setattr(category, 'diff', category_obj.get_diff())
    setattr(category, 'goal_met', category_obj.get_goal_met())

    return category

@router.put("/{id}", response_model=schemas.CategoryOut)
def update_category(id: int, updated_category: schemas.CategoryIn, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    category_query = db.query(models.Category).filter(models.Category.id == id)

    category = category_query.first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id: {id} does not exist")

    if category.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    updated_category_header_id = db.query(models.Header.id).filter(models.Header.name == updated_category.header).first()

    if updated_category_header_id == None and updated_category.type == 'Expense':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A category without a header cannot be assigned to the type 'Expense'.")

    if updated_category_header_id != None and updated_category.type == 'Income':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A category with a header cannot be assigned the type 'Income'.")

    
    
    category_query.update(updated_category.dict(), synchronize_session=False)
    db.commit()

    def category_id_update(query, header_name: str, header_id: int):

        category = query.first()

        # if header_id != None and header_name == "":
        category.header_name = header_name
        category.header_id = header_id[0]

        new_category = schemas.CategoryOutDB(id = category.id, name = category.name, planned=category.planned, goal=category.goal, type=category.type, header=category.header, header_id=category.header_id)
        
        query.update(new_category.dict(), synchronize_session=False)
        db.commit()

    category_id_update(category_query, updated_category.header, updated_category_header_id)

    new_updated_category = category_query.first()

    actual_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.category == category.name).first()

    actual = actual_query[0]

    if actual == None:
        actual = 0

    category_obj = category_class.Category(new_updated_category.name, new_updated_category.planned, actual, new_updated_category.goal)

    setattr(new_updated_category, 'actual', category_obj.get_actual())
    setattr(new_updated_category, 'diff', category_obj.get_diff())
    setattr(new_updated_category, 'goal_met', category_obj.get_goal_met())

    return new_updated_category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    category_query = db.query(models.Category).filter(models.Category.id == id)

    category = category_query.first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id: {id} does not exist")

    if category.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    category_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





