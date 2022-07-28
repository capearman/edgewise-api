import pytest
from app import schemas

last_month_balance_test_data = {
    "last_month_balance": 2000
}

def test_get_metrics_successful(authorized_client, test_headers, test_categories):
    result = authorized_client.get("/metrics/")
    assert result.status_code == 200

def test_get_metrics_negative_mtc(authorized_client, headers_for_metrics_testing1, categories_for_metrics_testing1, transactions_for_metrics_testing1):
    authorized_client.put(f"/last_month_balance/",json=last_month_balance_test_data)
    result = authorized_client.get("/metrics/")
    metrics = schemas.Metrics(**result.json())
    assert float(metrics.money_to_categorize) == -1269.71

def test_get_metrics_zero_mtc(authorized_client, headers_for_metrics_testing1, categories_for_metrics_testing2, transactions_for_metrics_testing2):
    authorized_client.put(f"/last_month_balance/",json=last_month_balance_test_data)
    result = authorized_client.get("/metrics/")
    metrics = schemas.Metrics(**result.json())
    assert float(metrics.money_to_categorize) == 0

def test_get_metrics_positive_current_balance(authorized_client, headers_for_metrics_testing1, categories_for_metrics_testing1, transactions_for_metrics_testing1):
    authorized_client.put(f"/last_month_balance/",json=last_month_balance_test_data)
    result = authorized_client.get("/metrics/")
    metrics = schemas.Metrics(**result.json())
    assert float(metrics.current_balance) == 6249.67