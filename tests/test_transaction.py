import pytest
from app import schemas

create_transaction_test_fields = "type, date, amount, description, category, check_box"
create_transaction_test_data = [
    ("Income", "2022-06-10", 2100.77, "Dead End Job", "Paycheck", False),
    ("Expense", "2022-06-03", 0.50, "Ramen", "Groceries", True),
    ("Expense", "2022-01-10", 200.55, "Plants", "Household Expenses", False),
]

create_multiple_transactions_in_one_category_data = [
    ("Expense", "2022-01-10", 200.55, "Testing multiple transactions in one category", "Household Expenses", False),
    ("Expense", "2022-01-10", 200.55, "Testing multiple transactions in one category", "Household Expenses", False),
]

update_transaction_test_data = {
        "id": 3,
        "type":"Income",
        "date": "2022-06-06",
        "amount": 333.21,
        "description": "Waffle House",
        "category": "Paycheck",
        "check_box": False
    }


def test_get_one_transaction_successful(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    assert result.status_code == 200

def test_unauthorized_user_get_one_transaction(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/transactions/{test_transactions[0].id}")
    assert result.status_code == 401

def test_get_one_transaction_id(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())
    assert transaction.id == test_transactions[0].id

def test_get_one_transaction_type(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())
    assert transaction.type == test_transactions[0].type

def test_get_one_transaction_date(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())
    assert transaction.date == test_transactions[0].date

def test_get_one_transaction_amount(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())
    assert transaction.amount == test_transactions[0].amount

def test_get_one_transaction_description(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())
    assert transaction.description == test_transactions[0].description

def test_get_one_transaction_category(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())
    assert transaction.category == test_transactions[0].category

def test_get_one_transaction_check_box(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/transactions/{test_transactions[0].id}")
    transaction = schemas.Transaction(**result.json())
    assert transaction.check_box == test_transactions[0].check_box

def test_get_one_transaction_not_exist(authorized_client):
    result = authorized_client.get("/transactions/999999999")
    assert result.status_code == 404

def test_get_all_transactions_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/transactions/")
    assert result.status_code == 200

def test_unauthorized_user_get_all_transactions(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/transactions/")
    assert result.status_code == 401

def test_get_all_transactions_that_exist_for_user(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/transactions/")
    assert len(result.json()) == 10

def test_get_all_transactions_that_exist_validate(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/transactions/")
    transactions = result.json()

    def validate(transaction):
        return schemas.Transaction(**transaction)
    
    for transaction in transactions:
        assert validate(transaction)


@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_create_transaction_successful(authorized_client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = authorized_client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})

    assert result.status_code == 201

@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_unauthorized_user_create_transaction(client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})

    assert result.status_code == 401

# @pytest.mark.parametrize(create_transaction_test_fields, create_multiple_transactions_in_one_category_data)
# def test_create_multiple_transactions_in_one_category_successful(client, test_headers, test_categories, type, date, amount, description, category, check_box):
#     result = client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})

#     assert result.status_code == 201

@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_create_transaction_type(authorized_client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = authorized_client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})
    created_transaction = schemas.TransactionCreateOut(**result.json())

    assert created_transaction.type == type

@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_create_transaction_date(authorized_client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = authorized_client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})
    created_transaction = schemas.TransactionCreateOut(**result.json())

    assert created_transaction.date.strftime('%Y-%m-%d') == date

@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_create_transaction_amount(authorized_client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = authorized_client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})
    created_transaction = schemas.TransactionCreateOut(**result.json())

    assert float(created_transaction.amount) == amount

@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_create_transaction_description(authorized_client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = authorized_client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})
    created_transaction = schemas.TransactionCreateOut(**result.json())

    assert created_transaction.description == description

@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_create_transaction_category(authorized_client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = authorized_client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})
    created_transaction = schemas.TransactionCreateOut(**result.json())

    assert created_transaction.category == category

@pytest.mark.parametrize(create_transaction_test_fields, create_transaction_test_data)
def test_create_transaction_check_box(authorized_client, test_headers, test_categories, type, date, amount, description, category, check_box):
    result = authorized_client.post("/transactions/", json={"type":type, "date":date, "amount":amount, "description":description, "category":category, "check_box":check_box})
    created_transaction = schemas.TransactionCreateOut(**result.json())

    assert created_transaction.check_box == check_box

def test_delete_transaction_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.delete(f"/transactions/{test_transactions[0].id}")
    assert result.status_code == 204

def test_other_user_delete_transaction(authorized_client, test_user, test_headers, test_categories, test_transactions):
    result = authorized_client.delete(f"/transactions/{test_transactions[10].id}")
    assert result.status_code == 403

def test_unauthorized_user_delete_transaction(client, test_headers, test_categories, test_transactions):
    result = client.delete(f"/transactions/{test_transactions[0].id}")
    assert result.status_code == 401

def test_delete_transaction_non_exist(authorized_client):
    result = authorized_client.delete("/transactions/9999999999")
    assert result.status_code == 404

def test_update_transaction_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    assert result.status_code == 200

def test_unauthorized_user_update_transaction(client, test_headers, test_categories, test_transactions):
    result = client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    assert result.status_code == 401

def test_other_user_update_transaction(authorized_client, test_user, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[10].id}", json=update_transaction_test_data)
    assert result.status_code == 403

def test_update_transaction_type(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    updated_transaction = schemas.TransactionUpdate(**result.json())
    assert updated_transaction.type == update_transaction_test_data['type']

def test_update_transaction_date(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    updated_transaction = schemas.TransactionUpdate(**result.json())
    assert updated_transaction.date.strftime('%Y-%m-%d') == update_transaction_test_data['date']

def test_update_transaction_amount(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    updated_transaction = schemas.TransactionUpdate(**result.json())
    assert float(updated_transaction.amount) == update_transaction_test_data['amount']

def test_update_transaction_description(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    updated_transaction = schemas.TransactionUpdate(**result.json())
    assert updated_transaction.description == update_transaction_test_data['description']

def test_update_transaction_category(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    updated_transaction = schemas.TransactionUpdate(**result.json())
    assert updated_transaction.category == update_transaction_test_data['category']

def test_update_transaction_check_box(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=update_transaction_test_data)
    updated_transaction = schemas.TransactionUpdate(**result.json())
    assert updated_transaction.check_box == update_transaction_test_data['check_box']

def test_update_transaction_non_exist(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put("/transactions/99999999",json=update_transaction_test_data)
    assert result.status_code == 404   

def test_update_id(authorized_client, test_headers, test_categories, test_transactions):
    data = {
        "id": 99,
        "type": "Expense",
        "date": "2022-06-07",
        "amount": float(33.21),
        "description": "Waffle House",
        "category": "Date Night",
        "category_id":3,
        "check_box": True
    }

    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=data)
    updated_transaction = schemas.TransactionReadOnly(**result.json())

    second_result = authorized_client.get(f"/transactions/{test_transactions[3].id}")
    second_transaction = schemas.Transaction(**second_result.json())

    assert updated_transaction.id == second_transaction.id

def test_update_category_id(authorized_client, test_headers, test_categories, test_transactions):
    data = {
        "id": 3,
        "type": "Expense",
        "date": "2022-06-07",
        "amount": float(33.21),
        "description": "Waffle House",
        "category": "Date Night",
        "category_id":1, #the category_id of Date Night is 3
        "check_box": True
    }

    result = authorized_client.put(f"/transactions/{test_transactions[3].id}",json=data)
    updated_transaction = schemas.TransactionReadOnly(**result.json())

    assert updated_transaction.category_id == 3

    





