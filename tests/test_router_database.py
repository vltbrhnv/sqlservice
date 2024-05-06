from httpx import AsyncClient

from tests.conftest import client


# async def test_create_db(ac:AsyncClient):
#     user_id = 1
#     token = "asdfghjkolmbhjvgcr"
#     response = await ac.post("/database/create_database", data = {"new_database":"db"})
#     assert response.status_code == 200
#     assert response.json()["status"] == "success"