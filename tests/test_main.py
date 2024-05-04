import pytest
from fastapi.testclient import TestClient

from conftest import client
from src.main import app

def test_register():
    user_data = {"email": "testing@mail.ru", "password": "parol", "is_active": True,  "is_superuser": False,
                 "is_verified": False, "username": "rabotay", "lastname": "last",  "firstname": "first"}
    response = client.post("/auth/register", json=user_data)
    response_bad = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json() == { "id": 1, "email": "testing@mail.ru", "is_active": True, "is_superuser": False,
              "is_verified": False, "username": "rabotay","lastname": "last", "firstname": "first"}
    assert response_bad.status_code == 400
    assert response_bad.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"

def test_login():
    response = client.post("/auth/jwt/login", data = {"username":"testing@mail.ru", "password": "parol"})
    response_bad_login = client.post("/auth/jwt/login", data={"username": "rabotay", "password": "parol"})
    response_bad_password = client.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "password"})
    response_bad_data = client.post("/auth/jwt/login", data={"username": "testing@mail.ru"})
    assert response.status_code == 204
    assert response_bad_login.status_code == 400
    assert response_bad_login.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_password.status_code == 400
    assert response_bad_password.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_data.status_code == 422




