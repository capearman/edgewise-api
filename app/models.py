from sqlalchemy import Column, Integer, String, Boolean, Numeric, DATE
from .database import Base

class Transaction(Base):
    __tablename__= "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    date = Column(DATE, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    check_box = Column(Boolean, server_default='FALSE', nullable=False)
    
