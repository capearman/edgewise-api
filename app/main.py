from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import transaction, category, header, metrics, user, auth, last_month_balance

tags_metadata = [
    {
        "name": "Metrics",
        "description": "Shows you your current balance and the money left to be categorized. The current balance value is not correct until every dollar has been categorized into the 'planned' field of the categories.",
    },
    {
        "name": "Last Month Balance",
        "description": "Your balance before the month began goes here.",
    },
    {
        "name": "Transactions",
        "description": "A transaction is every expense or income line item from your bank statement for the current month.",
    },
    {
        "name": "Categories",
        "description": "Every transaction belongs to a category. An example of a category would be 'Power Bill' or 'Groceries'.",
    },
    {
        "name": "Headers",
        "description": "Categories of type Expense belong to a header. An example of a header would be 'Bills' or 'Daily Expenses'.",
    },
    {
        "name": "Authentication",
        "description": "This endpoint is for authentication data but does not allow you to log in. To log in, use the 'Authorize' button at the top right side of this page.",
    }
]

app = FastAPI(
    title="EdgeWise API",
    description="An API that implements logic for a zero-based monthly budget. For 'backing away from the financial edge.'",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

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

# @app.get("/")
# async def root():
#     return {"message":"Prepare to budget your face off!"}

app.include_router(metrics.router)
app.include_router(last_month_balance.router)
app.include_router(transaction.router)
app.include_router(category.router)
app.include_router(header.router)
app.include_router(user.router)
app.include_router(auth.router)


