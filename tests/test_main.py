from httpx import AsyncClient

user_data = {"email": "testing@mail.ru", "password": "parol", "is_active": True, "is_superuser": False,
             "is_verified": False, "username": "test_user", "lastname": "last", "firstname": "first"}

async def test_register(ac: AsyncClient):
    response = await ac.post("/auth/register", json=user_data)
    response_bad = await ac.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json() == { "id": 1, "email": "testing@mail.ru", "is_active": True, "is_superuser": False,
                                "is_verified": False, "username": "test_user","lastname": "last", "firstname": "first"}
    assert response_bad.status_code == 400
    assert response_bad.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"

async def test_login(ac: AsyncClient):
    response = await ac.post("/auth/jwt/login", data = {"username":"testing@mail.ru", "password": "parol"})
    response_bad_login = await ac.post("/auth/jwt/login", data={"username": "test_user", "password": "parol"})
    response_bad_password = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "password"})
    response_bad_data = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru"})
    assert response.status_code == 200
    assert response_bad_login.status_code == 400
    assert response_bad_login.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_password.status_code == 400
    assert response_bad_password.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert response_bad_data.status_code == 422

async def test_logout(ac: AsyncClient):
    login_response = await ac.post("/auth/jwt/login", data = {"username":"testing@mail.ru", "password": "parol"})
    token = login_response.json()['access_token']
    response = await ac.post("/auth/jwt/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204
    token_bad = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE3MTU2MzUwMTZ9.4Dz3IrOcH3f5sGO5W43vdZt2bbyZpzeOMukuygMZtpu"
    response_bad = await ac.post("/auth/jwt/logout", headers={"Authorization": f"Bearer {token_bad}"})
    assert response_bad.status_code == 401
    assert response_bad.json()["detail"] == 'Invalid token'


