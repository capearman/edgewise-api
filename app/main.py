from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import transaction, category, header, metrics, user, auth

app = FastAPI()

#CORS stuff
#TODO: Change this upon deployment?
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message":"Prepare to budget your face off!"}

app.include_router(transaction.router)
app.include_router(category.router)
app.include_router(header.router)
app.include_router(metrics.router)
app.include_router(user.router)
app.include_router(auth.router)

