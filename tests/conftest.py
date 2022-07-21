from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, null
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import models
from fastapi import Depends

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

def pass_to_db(data, model, session):
    def create_model(data):
        return model(**data)

    data_map = map(create_model, data)
    data_list = list(data_map)

    session.add_all(data_list)
    session.commit()

def fetch_data(model, session):
    data = session.query(model).all()
    return data

@pytest.fixture()
def test_headers(session):
    headers_data = [
        {
            "id":1,
            "name": "Bills",
        },
        {
            "id":2,
            "name": "Daily",
        },
        {
            "id":3,
            "name": "Long Term",
        },
        {
            "id":4,
            "name": "Count My Categories!",
        }]

    pass_to_db(headers_data, models.Header, session)
    return fetch_data(models.Header, session)

@pytest.fixture()
def test_categories(session):
    categories_data = [
        {
           "id":1,
           "name":"Paycheck",
           "planned":0,
           "goal":0,
           "type": "Income",
        },
        {
            "id":2,
            "name":"Groceries",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Daily",
            "header_id":2,
        },
        {
            "id":3,
            "name":"Date Night",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Daily",
            "header_id":2,
        },
        {
            "id":4,
            "name":"Household Expenses",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Long Term",
            "header_id":3,
        },
        {
           "id":5,
           "name":"No Transactions",
           "planned":0,
           "goal":0,
           "type": "Income",
        },
        {
           "id":6,
           "name":"Testing Category Actual",
           "planned":0,
           "goal":0,
           "type": "Income",
        },
        {
           "id":7,
           "name":"Testing Category Diff",
           "planned":40,
           "goal":0,
           "type": "Income",
        },
        {
           "id":8,
           "name":"Testing Category Diff Negative",
           "planned":5,
           "goal":0,
           "type": "Income",
        },
        {
           "id":9,
           "name":"Testing Category Goal Met True Equal",
           "planned":5,
           "goal":5,
           "type": "Income",
        },
        {
           "id":10,
           "name":"Testing Category Goal Met True Over",
           "planned":6,
           "goal":5,
           "type": "Income",
        },
        {
           "id":11,
           "name":"Testing Category Goal Met False",
           "planned":4,
           "goal":5,
           "type": "Income",
        },
        {
            "id":12,
            "name":"Cat1",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Count My Categories!",
            "header_id":4,
        },
        {
            "id":13,
            "name":"Cat2",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Count My Categories!",
            "header_id":4,
        },
        {
            "id":14,
            "name":"Cat3",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Count My Categories!",
            "header_id":4,
        },
        {
            "id":15,
            "name":"Cat4",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Count My Categories!",
            "header_id":4,
        },
        {
            "id":16,
            "name":"Testing change type from Expense to Income with a header assigned",
            "planned":100,
            "goal":200,
            "type": "Expense",
            "header":"Long Term",
            "header_id":3,
        }]

    pass_to_db(categories_data, models.Category, session)
    return fetch_data(models.Category, session)

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
            "category_id":1,
            "check_box": False

        },
        {
            "id": 1,
            "type": "Income",
            "date": "2022-06-20",
            "amount": float(2010.59),
            "description": "Second software engineer paycheck",
            "category": "Paycheck",
            "category_id":1,
            "check_box": False

        },
        {
            "id": 2,
            "type": "Expense",
            "date": "2022-06-06",
            "amount": float(43.55),
            "description": "Aldi",
            "category": "Groceries",
            "category_id":2,
            "check_box": True

        },
        {
            "id": 3,
            "type": "Expense",
            "date": "2022-06-07",
            "amount": float(33.21),
            "description": "Waffle House",
            "category": "Date Night",
            "category_id":3,
            "check_box": True

        },
        {
            "id": 4,
            "type": "Expense",
            "date": "2022-06-08",
            "amount": float(8.08),
            "description": "Deli Sandwich",
            "category": "Groceries",
            "category_id":2,
            "check_box": False

        },
        {
            "id": 5,
            "type": "Expense",
            "date": "2022-06-10",
            "amount": float(40.77),
            "description": "Pillows",
            "category": "Household Expenses",
            "category_id":4,
            "check_box": True

        },
        {
            "id": 6,
            "type": "Expense",
            "date": "2022-06-10",
            "amount": float(5),
            "description": "testing category actual == 10",
            "category": "Testing Category Actual",
            "category_id":6,
            "check_box": True

        },
        {
            "id": 7,
            "type": "Expense",
            "date": "2022-06-10",
            "amount": float(5),
            "description": "testing category actual == 10",
            "category": "Testing Category Actual",
            "category_id":6,
            "check_box": True

        },
        {
            "id": 8,
            "type": "Expense",
            "date": "2022-06-10",
            "amount": float(20),
            "description": "testing category diff",
            "category": "Testing Category Diff",
            "category_id":7,
            "check_box": True

        },
        {
            "id": 9,
            "type": "Expense",
            "date": "2022-06-10",
            "amount": float(10),
            "description": "testing category diff negative",
            "category": "Testing Category Diff Negative",
            "category_id":8,
            "check_box": True

        },]

    pass_to_db(transactions_data, models.Transaction, session)
    return fetch_data(models.Transaction, session)