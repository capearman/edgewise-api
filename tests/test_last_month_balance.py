import pytest
from app import schemas

last_month_balance_test_data = {
    "last_month_balance": 2034.55
}

def test_update_balance_success(authorized_client, test_user):
    result = authorized_client.put(f"/last_month_balance/",json=last_month_balance_test_data)
    assert result.status_code == 200

def test_unauthenticated_user_update_balance(client, test_user):
    result = client.put(f"/last_month_balance/",json=last_month_balance_test_data)
    assert result.status_code == 401

def test_update_balance_value(authorized_client, test_user):
    result = authorized_client.put(f"/last_month_balance/",json=last_month_balance_test_data)
    assert result.json() == last_month_balance_test_data

def test_get_balance_success(authorized_client, test_user2):
    result = authorized_client.get("/last_month_balance/")
    assert result.status_code == 200

def test_unauthenticated_user_get_balance(client, test_user2):
    result = client.get("/last_month_balance/")
    assert result.status_code == 401

def test_get_balance_value(authorized_client):
    authorized_client.put(f"/last_month_balance/",json=last_month_balance_test_data)
    result = authorized_client.get("/last_month_balance/")
    assert result.json() == last_month_balance_test_data