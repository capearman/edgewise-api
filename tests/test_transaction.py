import pytest
from app import schemas
import datetime

def test_get_one_transaction(client, test_transactions):
    result = client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())

    assert transaction.id == test_transactions[0].id
    assert transaction.type == test_transactions[0].type
    assert transaction.date == test_transactions[0].date
    assert transaction.amount == test_transactions[0].amount
    assert transaction.description == test_transactions[0].description
    assert transaction.category == test_transactions[0].category
    assert transaction.check_box == test_transactions[0].check_box

def test_get_one_transaction_not_exist(client):
    result = client.get("/transactions/999999999")
    assert result.status_code == 404

def test_get_all_transactions(client, test_transactions):
    result = client.get("/transactions/")

    def validate(transaction):
        return schemas.Transaction(**transaction)
    
    transaction_map = map(validate, result.json())
    transaction_list = list(transaction_map)

    assert len(result.json()) == len(test_transactions)
    assert result.status_code == 200

@pytest.mark.parametrize("type, date, amount, description, category, check_box",[
    ("Income", "2022-06-10", 2100.77, "Dead End Job", "Paycheck", False),
    ("Expense", "2022-06-03", 0.50, "Ramen", "Groceries", True),
    ("Expense", "2022-01-10", 200.55, "New Tires", "Car Expenses", False)
])
def test_create_transaction(client, type, date, amount, description, category, check_box):
    result = client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})
    print(f"...result: {result}")
    created_transaction = schemas.TransactionCreate(**result.json())

    assert result.status_code == 201
    assert created_transaction.type == type
    assert created_transaction.date.strftime('%Y-%m-%d') == date
    assert float(created_transaction.amount) == amount
    assert created_transaction.description == description
    assert created_transaction.category == category
    assert created_transaction.check_box == check_box

def test_delete_transaction_success(client, test_transactions):
    result = client.delete(f"/transactions/{test_transactions[0].id}")
    assert result.status_code == 204

def test_delete_transaction_non_exist(client):
    result = client.delete("/transactions/9999999999")
    assert result.status_code == 404

def test_update_transaction(client, test_transactions):
    data = {
        "id":test_transactions[3].id,
        "type":"Income",
        "date": "2022-06-06",
        "amount": 333.21,
        "description": "Waffle House",
        "category": "First Paycheck",
        "check_box": False
    }

    result = client.put(f"/transactions/{test_transactions[3].id}",json=data)
    updated_transaction = schemas.Transaction(**result.json())

    assert updated_transaction.id == data['id']
    assert updated_transaction.type == data['type']
    assert updated_transaction.date.strftime('%Y-%m-%d') == data['date']
    assert float(updated_transaction.amount) == data['amount']
    assert updated_transaction.description == data['description']
    assert updated_transaction.category == data['category']
    assert updated_transaction.check_box == data['check_box']

def test_update_transaction_non_exist(client, test_transactions):
    data = {
        "id":test_transactions[3].id,
        "type":"Income",
        "date": "2022-06-06",
        "amount": 333.21,
        "description": "Waffle House",
        "category": "First Paycheck",
        "check_box": False
    }

    result = client.put("/transactions/99999999",json=data)

    assert result.status_code == 404





   





    