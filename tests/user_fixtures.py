from main import app
import pytest
import random
import string
from httpx import AsyncClient
from sqlalchemy.orm import Session
from conf_test_db import override_db_session


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://test/"


@pytest.fixture(scope="session")
def test_client(base_url) -> AsyncClient:
    return AsyncClient(app=app, base_url=base_url)


@pytest.fixture(scope="session")
def database() -> Session:
    return next(override_db_session())


@pytest.fixture(scope="function")
def credentials() -> dict[str: str]:
    credentials = {}
    credentials["login"] = "".join(random.choices(string.ascii_letters + string.digits,
                                                  k=random.randint(2, 50)
                                                  )
                                   ).lower()
    credentials["password"] = "".join(random.choices(string.ascii_letters + string.digits,
                                                     k=random.randint(8, 100)
                                                     )
                                      )
    return credentials


@pytest.fixture(scope="function")
async def access_token(test_client, credentials) -> str:
    token_login = credentials["login"]
    token_password = credentials["password"]
    registered = await test_client.post("user/new",
                                        json={"login": token_login,
                                              "password": token_password,
                                              }
                                        )
    assert registered.status_code == 200
    response = await test_client.post("token",
                                      headers={"username": token_login,
                                               "password": token_password,
                                               }
                                      )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token
