from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, DATE, TIMESTAMP, text
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
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class Category(Base):
    __tablename__= "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    planned = Column(Numeric, nullable=False)
    goal = Column(Numeric, nullable=False)
    type = Column(String, nullable=False)
    header = Column(String, nullable=True)
    header_id = Column(Integer, ForeignKey("headers.id", ondelete="CASCADE"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class Header(Base):
    __tablename__="headers"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_month_balance = Column(Numeric, server_default=text('0'), nullable=False)