import pytest
from app import schemas

def test_get_metrics_successful(client, test_headers, test_categories):
    result = client.get("/metrics/")
    assert result.status_code == 200

def test_get_metrics_negative_mtc(client, headers_for_metrics_testing_mtc_negative, categories_for_metrics_testing_mtc_negative, transactions_for_metrics_testing_mtc_negative):
    result = client.get("/metrics/")
    metrics = schemas.Metrics(**result.json())
    assert float(metrics.money_to_categorize) == -1269.71