from typing import List, Optional
from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/headers",
    tags=['Headers']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.HeaderOut)
def create_header(header: schemas.HeaderIn, db:Session = Depends(get_db)):
    new_header = models.Header(**header.dict())
    
    db.add(new_header)
    db.commit()
    db.refresh(new_header)
    return new_header

@router.put("/{id}", response_model=schemas.HeaderOut)
def update_header(id: int, updated_header: schemas.HeaderIn, db: Session = Depends(get_db)):
    header_query = db.query(models.Header).filter(models.Header.id == id)
    header = header_query.first()

    if header == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"header with id {id} does not exist.")

    header_query.update(updated_header.dict(), synchronize_session=False)
    db.commit()
    return header_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_header(id: int, db: Session = Depends(get_db)):
    header_query = db.query(models.Header).filter(models.Header.id == id)
    header = header_query.first()

    if header == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"header with id {id} does not exist.")

    header_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", response_model=List[schemas.Header])
def get_headers(db: Session = Depends(get_db)):
    
    headers = db.query(models.Header).all()
    return headers

@router.get("/{id}", response_model=schemas.HeaderOut)
def get_header(id: int, db: Session = Depends(get_db)):
    header = db.query(models.Header).filter(models.Header.id == id).first()

    if not header:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"header with id {id} does not exist.")

    return header