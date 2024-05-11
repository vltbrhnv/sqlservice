from httpx import AsyncClient

async def test_get_user_info(ac: AsyncClient):
    login_response = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "parol"})
    token = login_response.json()['access_token']
    response = await ac.get("/user/get_user_info/", headers={"token": token})
    response_bad = await ac.get("/user/get_user_info/", headers={"token": "1234"})
    assert response.status_code == 200
    assert response_bad.status_code == 401
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


