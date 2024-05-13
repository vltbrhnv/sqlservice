from httpx import AsyncClient

async def test_get_user_info(ac: AsyncClient):
    login_response = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "parol"})
    token = login_response.json()['access_token']
    token_bad = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE3MTU2MzUwMTZ9.4Dz3IrOcH3f5sGO5W43vdZt2bbyZpzeOMukuygMZtpu"
    response = await ac.get("/user/get_user_info/1", headers={"token": token})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {
                              "status": "success",
                              "data": [
                                {
                                  "email": "testing@mail.ru",
                                  "username:": "test_user",
                                  "lastname": "last",
                                  "firstname": "first"
                                }
                              ]
                            }
    response_bad = await ac.get("/user/get_user_info/1", headers={"token": token_bad})
    assert response_bad.status_code == 401
    assert response_bad.json() == {"detail": "Invalid token"}


