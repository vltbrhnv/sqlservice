import datetime
from typing import Annotated

import jwt
from fastapi import Header

from conftest import client
from src.config import SECRET_AUTH

user_data = {"email": "testing@mail.ru", "password": "parol", "is_active": True, "is_superuser": False,
             "is_verified": False, "username": "rabotay", "lastname": "last", "firstname": "first"}
def generate_token(SECRET_AUTH):
    payload = { "user_id": 1,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)}
    token = jwt.encode(payload, SECRET_AUTH, algorithm="HS256")
    return token
fake_token = generate_token(SECRET_AUTH)

def test_register():
    response = client.post("/auth/register", json=user_data)
    response_bad = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json() == { "id": 1, "email": "testing@mail.ru", "is_active": True, "is_superuser": False,
                                "is_verified": False, "username": "rabotay","lastname": "last", "firstname": "first"}
    assert response_bad.status_code == 400
    assert response_bad.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"

def test_login():
    response = client.post("/auth/jwt/login", data = {"username":"testing@mail.ru", "password": "parol"},
                           headers={"Authorization": f"Bearer {fake_token}", "Token": fake_token})
    response_bad_login = client.post("/auth/jwt/login", data={"username": "rabotay", "password": "parol"})
    response_bad_password = client.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "password"})
    response_bad_data = client.post("/auth/jwt/login", data={"username": "testing@mail.ru"})
    assert response.status_code == 204
    assert response_bad_login.status_code == 400
    assert response_bad_login.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_password.status_code == 400
    assert response_bad_password.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_data.status_code == 422

def test_logout():
    response = client.post("/auth/jwt/logout", headers={"Authorization": f"Bearer {fake_token}", "Token": fake_token})
    assert response.status_code == 200



