from json import dumps

import pytest
from httpx import AsyncClient

from tests.conftest import client
from conftest import client, async_session_maker

def test_register():
    user_data = {
    "email": "pochtamy@bk.ru",
    "password": "password",
    "is_active": True,
    "is_superuser": False,
    "is_verified": False,
    "username": "rabotay",
    "lastname": "last",
    "firstname": "first"
    }
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201


# @pytest.mark.asyncio
# async def test_register(ac: AsyncClient):
#     user_data = {
#     "email": "pochtamy@bk.ru",
#     "password": "password",
#     "is_active": True,
#     "is_superuser": False,
#     "is_verified": False,
#     "username": "rabotay",
#     "lastname": "last",
#     "firstname": "first"
#     }
#     response = await ac.post("/auth/register", json=user_data)
#
#     assert response.status_code == 201


