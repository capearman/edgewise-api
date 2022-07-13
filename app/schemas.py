from pydantic import BaseModel, condecimal
from typing import Literal
from datetime import date

class TransactionBase(BaseModel):
    id: int
    type: Literal['Income', 'Expense'] #expense or income
    date: date
    amount: condecimal(gt=0, max_digits=10, decimal_places=2) 
    description: str
    category: str
    check_box: bool #for keeping track of what has been logged if looking at bank statement

    class Config:
        orm_mode = True

class Transaction(TransactionBase):
    pass

    class Config:
        orm_mode = True    

class TransactionCreateIn(BaseModel):
    type: Literal['Income', 'Expense'] 
    date: date
    amount: condecimal(gt=0, max_digits=10, decimal_places=2) 
    description: str
    category: str
    check_box: bool = False #for keeping track of what has been logged if looking at bank statement

    class Config:
        orm_mode = True

class TransactionCreateOut(BaseModel):
    id: int
    type: Literal['Income', 'Expense'] 
    date: date
    amount: condecimal(gt=0, max_digits=10, decimal_places=2) 
    description: str
    category: str
    category_id: int
    check_box: bool = False #for keeping track of what has been logged if looking at bank statement

    class Config:
        orm_mode = True

class TransactionReadOnly(BaseModel):
    id: int
    type: Literal['Income', 'Expense'] 
    date: date
    amount: condecimal(gt=0, max_digits=10, decimal_places=2) 
    description: str
    category: str
    category_id: int
    check_box: bool = False #for keeping track of what has been logged if looking at bank statement

    class Config:
        orm_mode = True

class TransactionUpdate(BaseModel):
    type: Literal['Income', 'Expense'] 
    date: date
    amount: condecimal(gt=0, max_digits=10, decimal_places=2) 
    description: str
    category: str
    check_box: bool = False #for keeping track of what has been logged if looking at bank statement

    class Config:
        orm_mode = True

class CategoryOut(BaseModel):
    id: int
    name: str
    planned: condecimal(ge=0, max_digits=10, decimal_places=2)
    actual: condecimal(ge=0, max_digits=10, decimal_places=2)
    diff: condecimal(max_digits=10, decimal_places=2)
    goal: condecimal(ge=0, max_digits=10, decimal_places=2)
    goal_met: bool
    type: Literal['Income', 'Expense'] 

    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str
    planned: condecimal(gt=0, max_digits=10, decimal_places=2)
    goal: condecimal(ge=0, max_digits=10, decimal_places=2)
    type: Literal['Income', 'Expense'] 

    class Config:
        orm_mode = True

class CategoryName(BaseModel):
    name: str

    class Config:
        orm_mode = True



