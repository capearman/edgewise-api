from pydantic import BaseModel
from datetime import date

class Transaction(BaseModel):
    id: int
    type: str #expense or income
    date: date
    amount: float
    description: str
    category: str
    check_box: bool #for keeping track of what has been logged if looking at bank statement

    class Config:
        orm_mode = True

