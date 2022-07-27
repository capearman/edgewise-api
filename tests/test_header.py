import pytest
from app import schemas

create_header_test_field = "name"
create_header_test_data = [
    ("Goat Expenses"),
    ("Sandwich Expenses"),
    ("Drywall Eating Addiction"),
]

update_header_test_data = {
    "id":55,
    "name":"Childcare Expenses",
}

def test_get_one_header_successful(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/headers/{test_headers[0].id}")
    assert result.status_code == 200

def test_unauthorized_user_get_one_header(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/headers/{test_headers[0].id}")
    assert result.status_code == 401

def test_get_one_header_id(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/headers/{test_headers[0].id}")
    header = schemas.Header(**result.json())
    assert header.id == test_headers[0].id

def test_get_one_header_name(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/headers/{test_headers[0].id}")
    header = schemas.Header(**result.json())
    assert header.name == test_headers[0].name

def test_get_all_headers_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/headers/")
    assert result.status_code == 200

def test_unauthenticated_user_get_all_headers(client, test_headers, test_categories, test_transactions):
    result = client.get("/headers/")
    assert result.status_code == 401

def test_get_all_headers_that_exist_for_user(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/headers/")
    assert len(result.json()) == 4

def test_get_all_headers_that_exist_validate(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/headers/")
    headers = result.json()

    def validate(header):
        return schemas.Header(**header)
    
    for header in headers:
        assert validate(header)

@pytest.mark.parametrize(create_header_test_field, create_header_test_data)
def test_create_header_successful(authorized_client, name):
    result = authorized_client.post("/headers/", json={"name":name})
    assert result.status_code == 201

@pytest.mark.parametrize(create_header_test_field, create_header_test_data)
def test_unauthorized_user_create_header(client, name):
    result = client.post("/headers/", json={"name":name})
    assert result.status_code == 401

@pytest.mark.parametrize(create_header_test_field, create_header_test_data)
def test_create_header_name(authorized_client, name):
    result = authorized_client.post("/headers/", json={"name":name})
    print(f"\n\nresult: {result.json()}\n\n")
    created_header = schemas.HeaderIn(**result.json())

    assert created_header.name == name

def test_delete_header_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.delete(f"/headers/{test_headers[0].id}")
    assert result.status_code == 204

def test_unauthorized_user_delete_header(client, test_headers, test_categories, test_transactions):
    result = client.delete(f"/headers/{test_headers[0].id}")
    assert result.status_code == 401

def test_other_user_delete_header(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.delete(f"/headers/{test_headers[4].id}")
    assert result.status_code == 403

def test_delete_header_non_exist(authorized_client):
    result = authorized_client.delete("/headers/9999999999")
    assert result.status_code == 404

def test_update_header_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/headers/{test_headers[2].id}",json=update_header_test_data)
    assert result.status_code == 200

def test_unauthenticated_user_update_header(client, test_headers, test_categories, test_transactions):
    result = client.put(f"/headers/{test_headers[2].id}",json=update_header_test_data)
    assert result.status_code == 401

def test_other_user_update_header(authorized_client, test_user, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/headers/{test_headers[4].id}",json=update_header_test_data)
    assert result.status_code == 403

def test_update_header_name(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/headers/{test_headers[2].id}",json=update_header_test_data)
    updated_header = schemas.Header(**result.json())
    assert updated_header.name == update_header_test_data['name']

def test_get_all_categories_in_header_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/headers/categories/{test_headers[3].id}")
    assert result.status_code == 200

def test_unauthorized_user_get_all_categories_in_header(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/headers/categories/{test_headers[3].id}")
    assert result.status_code == 401

def test_get_all_categories_in_header_that_exist_for_user(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/headers/categories/{test_headers[3].id}")
    categories = result.json()['categories']
    print(f"\n\n...categories: {categories}...\n\n")
    assert len(categories) == 4

def test_get_all_categories_in_header_that_exist_validate(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/headers/categories/{test_headers[3].id}")
    header_categories = result.json()

    def validate(header_category):
        return schemas.HeaderCategories(**header_category)
    
    assert validate(header_categories)