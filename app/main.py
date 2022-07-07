from unicodedata import category
from fastapi import FastAPI
from .routers import transaction, category
from . import models
from .database import engine
from passlib.context import CryptContext

from . import schemas, category_class, models
from sqlalchemy.orm import Session
from fastapi import Request, Depends
from .database import get_db

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#models.Base.metadata.create_all(bind=engine) #don't need this after installing alembic. Creates tables when app starts up

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Prepare to budget your face off!"}

app.include_router(transaction.router)
app.include_router(category.router)

