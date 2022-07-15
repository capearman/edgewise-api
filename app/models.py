from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, DATE
from sqlalchemy.orm import relationship
from .database import Base

class Transaction(Base):
    __tablename__= "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    date = Column(DATE, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    check_box = Column(Boolean, server_default='FALSE', nullable=False)

class Category(Base):
    __tablename__= "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    planned = Column(Numeric, nullable=False)
    goal = Column(Numeric, nullable=False)
    type = Column(String, nullable=False)
    header = Column(String, nullable=True)
    header_id = Column(Integer, ForeignKey("headers.id", ondelete="CASCADE"), nullable=True)

class Header(Base):
    __tablename__="headers"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)