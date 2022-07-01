from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) # drop all tables
    Base.metadata.create_all(bind=engine) # create all tables

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture()
def client(session):
    def override_get_db():
        
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_transactions(session):
    transactions_data = [
        {
            "id": 0,
            "type": "Income",
            "date": "2022-06-19",
            "amount": float(2000.69),
            "description": "First software engineer paycheck",
            "category": "Paycheck",
            "check_box": False

        },
        {
            "id": 1,
            "type": "Income",
            "date": "2022-06-20",
            "amount": float(2010.59),
            "description": "Second software engineer paycheck",
            "category": "Paycheck",
            "check_box": False

        },
        {
            "id": 2,
            "type": "Expense",
            "date": "2022-06-06",
            "amount": float(43.55),
            "description": "Aldi",
            "category": "Groceries",
            "check_box": True

        },
        {
            "id": 3,
            "type": "Expense",
            "date": "2022-06-07",
            "amount": float(33.21),
            "description": "Waffle House",
            "category": "Date Night",
            "check_box": True

        },
        {
            "id": 4,
            "type": "Expense",
            "date": "2022-06-08",
            "amount": float(8.08),
            "description": "Deli Sandwich",
            "category": "Groceries",
            "check_box": False

        },
        {
            "id": 5,
            "type": "Expense",
            "date": "2022-06-10",
            "amount": float(40.77),
            "description": "Pillows",
            "category": "Household Expenses",
            "check_box": True

        },]

    def create_transaction_model(transaction):
        return models.Transaction(**transaction)

    transaction_map = map(create_transaction_model, transactions_data)
    transactions = list(transaction_map)

    session.add_all(transactions)
    session.commit()
    transactions = session.query(models.Transaction).all()

    return transactions