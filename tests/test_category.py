import pytest
from app import schemas

create_category_test_fields = "name, planned, goal, type, header, header_id"
create_category_test_data = [
    ("New Category",100,200,"Expense","Daily",2),
    ("Newer Category",200,200,"Expense","Daily",2),
    ("Newest Category",400,200,"Expense","Daily",2),
]


def test_get_one_category_successful(client, test_headers, test_categories):
    result = client.get(f"/categories/{test_categories[1].id}")
    assert result.status_code == 200

def test_get_one_category_id(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[0].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.id == test_categories[0].id

def test_get_one_category_name(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[0].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.name == test_categories[0].name

def test_get_one_category_actual(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[5].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.actual == 10

# when there are no transactions in a category, actual defaults to 0
def test_get_one_category_actual_is_none(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[4].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.actual == 0

def test_get_one_category_diff(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[6].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.diff == 20

def test_get_one_category_diff_negative(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[7].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.diff == -5

def test_get_one_category_planned(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[0].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.planned == test_categories[0].planned

def test_get_one_category_goal(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal == test_categories[1].goal

def test_get_one_category_goal_met_true_equal(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[8].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal_met == True

def test_get_one_category_goal_met_true_over(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[9].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal_met == True

def test_get_one_category_goal_met_false(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[10].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.goal_met == False

def test_get_one_category_type(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.type == test_categories[1].type

def test_get_one_category_header(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert category.header == test_categories[1].header

def test_get_one_category_header_id(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/{test_categories[1].id}")
    category = schemas.CategoryOut(**result.json())
    assert int(category.header_id) == test_categories[1].header_id

def test_get_one_category_not_exist(client, test_headers, test_categories, test_transactions):
    result = client.get(f"/categories/99999")
    assert result.status_code == 404

def test_get_all_categories_success(client, test_headers, test_categories, test_transactions):
    result = client.get("/categories/")
    assert result.status_code == 200

def test_get_all_categories_that_exist(client, test_headers, test_categories, test_transactions):
    result = client.get("/categories/")
    assert len(result.json()) == len(test_categories)

def test_get_all_categories_that_exist_validate(client, test_headers, test_categories, test_transactions):
    result = client.get("/categories/")
    categories = result.json()

    def validate(category):
        return schemas.CategoryOut(**category)
    
    for category in categories:
        assert validate(category)

def test_get_all_category_names_income_success(client, test_headers, test_categories, test_transactions):
    result = client.get('/categories/names/Income')
    assert result.status_code == 200

def test_get_all_category_names_expense_success(client, test_headers, test_categories, test_transactions):
    result = client.get('/categories/names/Expense')
    assert result.status_code == 200

def test_get_all_category_names_invalid_fail(client, test_headers, test_categories, test_transactions):
    result = client.get('/categories/names/Invalid')
    assert result.status_code == 404

@pytest.mark.parametrize(create_category_test_fields, create_category_test_data)
def test_create_category_success(client, test_headers, name, planned, goal, type, header, header_id):
    result = client.post("/categories/", json = {"name":name, "planned":planned, "goal":goal, "type":type, "header":header, "header_id":header_id})
    assert result.status_code == 201

@pytest.mark.parametrize(create_category_test_fields, create_category_test_data)
def test_create_category_without_header_success(client, test_headers, name, planned, goal, type, header, header_id):
    result = client.post("/categories/", json = {"name":name, "planned":planned, "goal":goal, "type":type, "header":"", "header_id": None})
    assert result.status_code == 201

