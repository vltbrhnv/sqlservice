from datetime import datetime, timedelta
import jwt
from httpx import AsyncClient
from src.config import SECRET_AUTH

user_data = {"email": "testing@mail.ru", "password": "parol", "is_active": True, "is_superuser": False,
             "is_verified": False, "username": "rabotay", "lastname": "last", "firstname": "first"}
def generate_token(SECRET_AUTH):
    data = {"sub": "1", "aud": ['fastapi-users:auth']}
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=3600)
    print(f'TEST_EXPIRE________{expire}')
    print(f'TEST_SUB________{1}')
    print(f'TEST_AUD________{['fastapi-users:auth']}')
    payload["exp"] = expire
    token = jwt.encode(payload, SECRET_AUTH, algorithm="HS256")
    return token

fake_token = generate_token(SECRET_AUTH=SECRET_AUTH)
async def test_register(ac: AsyncClient):
    response = await ac.post("/auth/register", json=user_data)
    response_bad = await ac.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json() == { "id": 1, "email": "testing@mail.ru", "is_active": True, "is_superuser": False,
                                "is_verified": False, "username": "rabotay","lastname": "last", "firstname": "first"}
    assert response_bad.status_code == 400
    assert response_bad.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"

async def test_login(ac: AsyncClient):
    response = await ac.post("/auth/jwt/login", data = {"username":"testing@mail.ru", "password": "parol"},
                             headers={"Authorization": f"Bearer {fake_token}", "Token": fake_token})
    response_bad_login = await ac.post("/auth/jwt/login", data={"username": "rabotay", "password": "parol"})
    response_bad_password = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "password"})
    response_bad_data = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru"})
    assert response.status_code == 204
    assert response_bad_login.status_code == 400
    assert response_bad_login.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_password.status_code == 400
    assert response_bad_password.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_data.status_code == 422

async def test_logout(ac: AsyncClient):
    print(f'FAKE_TOKEN____{fake_token}')
    response = await ac.post("/auth/jwt/logout", headers={"Authorization": f"Bearer {fake_token}", "Token": fake_token})
    assert response.status_code == 200



