import pytest
from jose import jwt
from app import schemas
from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Welcome to My FastAPI!!!"}


def test_create_user(client):
    response = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "hello123@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    # automatically add dummy data to test
    ("hellowkjk@gmail.com", "password123kdjkjd", 403),
    ("gairaladjkjdk@helod.com", "password123sks", 403),
    ("wrongmeial@gmail.com", "wrongpassword123", 403),
    (None, "gairalapassword123", 422),
    ("helosnkskj@gmail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
