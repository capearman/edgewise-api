import pytest
from app import schemas

create_category_test_fields = "name, planned, goal, type, header"
create_category_test_data = [
    ("New Category",100,200,"Expense","Daily"),
    ("Newer Category",200,200,"Expense","Bills"),
    ("Newest Category",400,200,"Expense","Long Term"),
]

create_category_without_header_test_data = [
    ("New Category",100,200,"Income","_"),
    ("Newer Category",200,200,"Income","_"),
    ("Newest Category",400,200,"Income","_"),
]

update_category_test_data = {
    "name": "Updated Category",
    "planned": 90,
    "goal": 40,
    "type": "Expense",
    "header": "Bills"
}

update_category_header_with_type_income_test_data = {
    "name": "Updated Category",
    "planned": 90,
    "goal": 40,
    "type": "Income",
    "header": "Bills"
}

create_multiple_categories_same_name = [
    ("Same Name",100,200,"Expense","Daily"),
    ("Same Name",200,200,"Income","Daily"),
]


def test_get_one_category_successful(authorized_client, test_headers, test_categories):
    result = authorized_client.get(f"/categories/{test_categories[1].id}")
    assert result.status_code == 200

def test_unauthorized_user_get_one_category(client, test_headers, test_categories):
    result = client.get(f"/categories/{test_categories[1].id}")
    assert result.status_code == 401

def test_get_one_category_id(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[0].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.id == test_categories[0].id

def test_get_one_category_name(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[0].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.name == test_categories[0].name

def test_get_one_category_actual(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[5].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.actual == 10

# when there are no transactions in a category, actual defaults to 0
def test_get_one_category_actual_is_none(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[4].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.actual == 0

def test_get_one_category_diff(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[6].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.diff == 20

def test_get_one_category_diff_negative(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[7].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.diff == -5

def test_get_one_category_planned(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[0].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.planned == test_categories[0].planned

def test_get_one_category_goal(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal == test_categories[1].goal

def test_get_one_category_goal_met_true_equal(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[8].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal_met == True

def test_get_one_category_goal_met_true_over(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[9].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal_met == True

def test_get_one_category_goal_met_false(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[10].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal_met == False

def test_get_one_category_type(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.type == test_categories[1].type

def test_get_one_category_header(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.header == test_categories[1].header

def test_get_one_category_header_id(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert int(category.header_id) == test_categories[1].header_id

def test_get_one_category_not_exist(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get(f"/categories/99999")
    assert result.status_code == 404

def test_get_all_categories_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/categories/")
    assert result.status_code == 200

def test_unauthorized_user_get_all_categories(client, test_headers, test_categories, test_transactions):
    result = client.get("/categories/")
    assert result.status_code == 401

def test_get_all_categories_that_exist_for_user(authorized_client, test_user, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/categories/")
    assert len(result.json()) == 16

def test_get_all_categories_that_exist_validate(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get("/categories/")
    categories = result.json()

    def validate(category):
        return schemas.CategoryOut(**category)
    
    for category in categories:
        assert validate(category)

def test_get_all_category_names_income_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get('/categories/names/Income')
    assert result.status_code == 200

def test_unauthorized_user_get_all_category_names_income(client, test_headers, test_categories, test_transactions):
    result = client.get('/categories/names/Income')
    assert result.status_code == 401

def test_get_all_category_names_expense_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get('/categories/names/Expense')
    assert result.status_code == 200

def test_unauthorized_user_get_all_category_names_expense(client, test_headers, test_categories, test_transactions):
    result = client.get('/categories/names/Expense')
    assert result.status_code == 401

def test_get_all_category_names_invalid_fail(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.get('/categories/names/Invalid')
    assert result.status_code == 404

@pytest.mark.parametrize(create_category_test_fields, create_category_test_data)
def test_create_category_success(authorized_client, test_headers, name, planned, goal, type, header):
    result = authorized_client.post("/categories/", json = {"name":name, "planned":planned, "goal":goal, "type":type, "header":header})
    assert result.status_code == 201

@pytest.mark.parametrize(create_category_test_fields, create_category_test_data)
def test_unauthorized_user_create_category(client, test_headers, name, planned, goal, type, header):
    result = client.post("/categories/", json = {"name":name, "planned":planned, "goal":goal, "type":type, "header":header})
    assert result.status_code == 401

# @pytest.mark.parametrize(create_category_test_fields, create_multiple_categories_same_name)
# def test_create_multiple_categories_same_name(client, test_headers, name, planned, goal, type, header):
#     result = client.post("/categories/", json = {"name":name, "planned":planned, "goal":goal, "type":type, "header":header})
#     assert result.status_code == 201

@pytest.mark.parametrize(create_category_test_fields, create_category_without_header_test_data)
def test_create_category_without_header_success(authorized_client, test_headers, name, planned, goal, type, header):
    result = authorized_client.post("/categories/", json = {"name":name, "planned":planned, "goal":goal, "type":type, "header":""})
    assert result.status_code == 201

def test_create_category_with_header_and_type_income(authorized_client, test_headers):
    result = authorized_client.post("/categories/", json = {"name":"Cat Expenses", "planned": 100, "goal": 200, "type": "Income", "header": "Bills"})
    assert result.status_code == 400

def test_create_category_without_header_and_type_expense(authorized_client):
    result = authorized_client.post("/categories/", json = {"name":"Cat Expenses", "planned": 100, "goal": 200, "type": "Expense", "header": ""})
    assert result.status_code == 400

def test_delete_category_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.delete(f"/categories/{test_categories[0].id}")
    assert result.status_code == 204

def test_unauthorized_user_delete_category(client, test_headers, test_categories, test_transactions):
    result = client.delete(f"/categories/{test_categories[0].id}")
    assert result.status_code == 401

def test_other_user_delete_category(authorized_client, test_headers, test_categories, test_transactions, test_user2):
    result = authorized_client.delete(f"/categories/{test_categories[16].id}")
    print(f"\n\nresult: {result.json()}\n\n")
    assert result.status_code == 403

def test_delete_category_non_exist(authorized_client):
    result = authorized_client.delete("/categories/9999999999")
    assert result.status_code == 404

def test_update_category_success(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[4].id}",json=update_category_test_data)
    assert result.status_code == 200

def test_unauthorized_user_update_category(client, test_headers, test_categories, test_transactions):
    result = client.put(f"/categories/{test_categories[4].id}",json=update_category_test_data)
    assert result.status_code == 401

def test_other_user_update_category(authorized_client, test_user, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[16].id}",json=update_category_test_data)
    assert result.status_code == 403

def test_update_category_name(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[3].id}",json=update_category_test_data)
    updated_category = schemas.CategoryOut(**result.json())
    assert updated_category.name == update_category_test_data['name']

def test_update_category_planned(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[3].id}",json=update_category_test_data)
    updated_category = schemas.CategoryOut(**result.json())
    assert updated_category.planned == update_category_test_data['planned']

def test_update_category_goal(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[3].id}",json=update_category_test_data)
    updated_category = schemas.CategoryOut(**result.json())
    assert updated_category.planned == update_category_test_data['planned']

def test_update_category_type(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[3].id}",json=update_category_test_data)
    updated_category = schemas.CategoryOut(**result.json())
    assert updated_category.type == update_category_test_data['type']

def test_update_category_header(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[3].id}",json=update_category_test_data)
    updated_category = schemas.CategoryOut(**result.json())
    assert updated_category.header == update_category_test_data['header']

def test_update_category_header_with_type_income(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[15].id}", json=update_category_header_with_type_income_test_data)
    assert result.status_code == 400

def test_update_category_without_header(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[15].id}", json={"name":"Cat Expenses", "planned": 100, "goal": 200, "type": "Expense", "header": ""})
    assert result.status_code == 400

def test_update_category_type_income_without_header(authorized_client, test_headers, test_categories, test_transactions):
    result = authorized_client.put(f"/categories/{test_categories[15].id}", json={"name":"Cat Expenses", "planned": 100, "goal": 200, "type": "Expense", "header": ""})
    assert result.status_code == 400
