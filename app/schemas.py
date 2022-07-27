from pydantic import BaseModel, condecimal, EmailStr
from typing import Literal
from datetime import date, datetime
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    id: int
    type: Literal['Income', 'Expense']  #expense or income
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
    header: Optional[str] = None
    header_id: Optional[str] = None

    class Config:
        orm_mode = True

class CategoryOutDB(BaseModel):
    id: int
    name: str
    planned: condecimal(ge=0, max_digits=10, decimal_places=2)
    goal: condecimal(ge=0, max_digits=10, decimal_places=2)
    type: Literal['Income', 'Expense'] 
    header: Optional[str] = None
    header_id: Optional[str] = None

    class Config:
        orm_mode = True

class CategoryIn(BaseModel):
    name: str
    planned: condecimal(ge=0, max_digits=10, decimal_places=2)
    goal: condecimal(ge=0, max_digits=10, decimal_places=2)
    type: Literal['Income', 'Expense']
    header: Optional[str] = None

    class Config:
        orm_mode = True

class CategoryName(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Header(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class HeaderIn(BaseModel):
    name: str

    class Config:
        orm_mode = True

class HeaderOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class HeaderCategories(BaseModel):
    id: int
    name: str

    categories: List[CategoryOut]

    class Config:
        orm_mode = True

class Metrics(BaseModel):
    money_to_categorize: condecimal(max_digits=10, decimal_places=2)
    current_balance: condecimal(max_digits=10, decimal_places=2)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None




