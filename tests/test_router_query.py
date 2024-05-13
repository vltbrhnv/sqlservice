from httpx import AsyncClient

async def test_query(ac: AsyncClient):
    login_response = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "parol"})
    token = login_response.json()['access_token']
    test_query_create = "CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(50), age INT );"
    response_insert = await ac.get("/query/query", params={"sqlquery": test_query_create},
                             headers={"token": token})
    assert response_insert.status_code == 200
    assert response_insert.json() ==  {"status": "success",
                                  "data": [ "Таблица была успешна создана"]}
    test_query_insert = "INSERT INTO test_table (id, name, age) VALUES (1, 'Анна', 25); INSERT INTO test_table (id, name, age) VALUES (2, 'Иван', 30); INSERT INTO test_table (id, name, age) VALUES (3, 'Мария', 28);"
    response_insert = await ac.get("/query/query", params={"sqlquery": test_query_insert},
                             headers={"token": token})
    assert response_insert.status_code == 200
    assert response_insert.json() ==  {
                              "status": "success",
                              "data": [
                                "В таблицу были успешно добaвлены данные",
                                "В таблицу были успешно добaвлены данные",
                                "В таблицу были успешно добaвлены данные"
                              ]
                            }
    test_query = "SELECT name FROM test_table WHERE id = 1"
    response_query = await ac.get("/query/query", params={"sqlquery": test_query},
                             headers={"token": token})
    assert response_query.status_code == 200
    assert response_query.json() ==  {
                              "status": "success",
                              "data": [ { "name": "Анна"}]
                            }
    test_query_create_bad = "CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(50), age INT );"
    response_create_bad = await ac.get("/query/query", params={"sqlquery": test_query_create_bad},
                             headers={"token": token})
    assert response_create_bad.json()["status"] == "error"
    test_query_bad = "SELECT job_id FROM test_table"
    response_query_bad = await ac.get("/query/query", params={"sqlquery": test_query_bad},
                             headers={"token": token})
    assert response_query_bad.json()["status"] == "error"
    test_bad = "SELECT name FROM countries"
    response_bad = await ac.get("/query/query", params={"sqlquery": test_bad},
                             headers={"token": token})
    assert response_bad.json()["status"] == "error"
    test_query_insert_bad = "INSERT INTO test_table (id, name, age) VALUES (1, 'Анна', 25); INSERT INTO test_table (id, name, age) VALUES (2, 'Иван', 30); INSERT INTO test_table (id, name, age) VALUES (3, 'Мария', 28);"
    response_insert_bad = await ac.get("/query/query", params={"sqlquery": test_query_insert_bad},
                             headers={"token": token})
    assert response_insert_bad.json()["status"] == "error"
    test_query_delete = "DELETE FROM test_table WHERE name = 'Иван';"
    response_delete = await ac.get("/query/query", params={"sqlquery": test_query_delete},
                             headers={"token": token})
    assert response_delete.status_code == 200
    assert response_delete.json() ==  {
                                      "status": "success",
                                      "data": [ "Из таблицы был успешно удален столбец" ] }


async def test_query_history(ac: AsyncClient):
    login_response = await ac.post("/auth/jwt/login", data={"username": "testing@mail.ru", "password": "parol"})
    token = login_response.json()['access_token']
    response = await ac.get("/query/query_history/1", headers={"token": token})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"] is not None
