import pytest
from jose import jwt
from app import schemas
from app.config import settings

def test_create_user_successful(client):
    result = client.post("/users/", json={"email":"cpearman@hotmails.com", "password":"beans123"})
    assert(result.status_code == 201)

def test_create_user_email(client):
    result = client.post("/users/", json={"email":"cpearman@hotmails.com", "password":"beans123"})
    new_user = schemas.UserOut(**result.json())
    assert new_user.email == "cpearman@hotmails.com"

def test_login_user_successful(client, test_user):
    result = client.post("/login", data={"username":test_user['email'], "password":test_user['password']})
    assert result.status_code == 200

def test_login_user_user_id(client, test_user):
    result = client.post("/login", data={"username":test_user['email'], "password":test_user['password']})

    login_res = schemas.Token(**result.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]) 
    id = payload.get("user_id")
    assert id == test_user['id']

def test_login_user_bearer_token(client, test_user):
    result = client.post("/login", data={"username":test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**result.json())
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'beans123', 403),
    ('cpearman@hotmails.com', 'wrongpassword', 403),
    (None, 'beans123', 422),
    ('cpearman@hotmails.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username":email, "password": password})

    assert res.status_code == status_code
