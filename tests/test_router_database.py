from httpx import AsyncClient

async def test_create_db(ac:AsyncClient):
    login_response = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "parol"})
    token = login_response.json()['access_token']
    response = await ac.post("/database/create_db_server", params = {"new_database":"test_database"}, headers={"token": token})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["details"] == "Создана база данных test_database"
    response_bad = await ac.post("/database/create_db_server", params={"new_database": "test_database"}, headers={"token": token})
    assert response_bad.status_code == 400
    assert response_bad.json()["detail"]["status"] == "error"
    assert response_bad.json()["detail"]["details"] == "Такая БД уже существует"
    response_new_database = await ac.post("/database/create_db_server", params = {"new_database":"new_test_database"}, headers={"token": token})
    assert response_new_database.status_code == 200
    assert response_new_database.json()["status"] == "success"
    assert response_new_database.json()["details"] =="Создана база данных new_test_database"
async def test_connect_to_db(ac:AsyncClient):
    login_response = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "parol"})
    token = login_response.json()['access_token']
    test_query_create = "CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(50), age INT );"
    demo_response = await ac.get("/query/query", params={"sqlquery": test_query_create},
                                   headers={"token": token})
    assert demo_response.status_code == 400
    assert demo_response.json() == {
                                      "detail": {
                                        "status": "error",
                                        "details": "Вы не подключены к базе данных"
                                      }
                                    }
    response = await ac.post("/database/connect_to_db/", params = {"dbname":"test_database"}, headers={"token": token})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["details"] =="Вы подключены к базе данных test_database"
    response_bad = await ac.post("/database/connect_to_db/", params={"dbname": "chepuha"}, headers={"token": token})
    assert response_bad.status_code == 489
    assert response_bad.json()["detail"]["status"] == "error"
    assert response_bad.json()["detail"]["details"] == "Такой базы данных не существует"