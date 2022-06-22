from fastapi import FastAPI
from .routers import transaction
from . import models
from .database import engine
from passlib.context import CryptContext

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine) #don't need this after installing alembic. Creates tables when app starts up

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Prepare to budget your face off!"}

app.include_router(transaction.router)

