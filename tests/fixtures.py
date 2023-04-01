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
    """Testing httpx client"""
    return AsyncClient(app=app, base_url=base_url)


@pytest.fixture(scope="session")
def database() -> Session:
    """Database session"""
    return next(override_db_session())


@pytest.fixture(scope="function")
def credentials() -> dict:
    """Create random login/password combos"""
    credentials = {
        "login": "".join(random.choices(string.ascii_letters + string.digits,
                                        k=random.randint(2, 50))).lower(),
        "password": "".join(random.choices(string.ascii_letters + string.digits,
                                           k=random.randint(8, 100)))
    }
    return credentials


@pytest.fixture(scope="function")
def another_credentials() -> dict:
    """Create random login/password combos"""
    another_credentials = {
        "login": "".join(random.choices(string.ascii_letters + string.digits,
                                        k=random.randint(2, 50))).lower(),
        "password": "".join(random.choices(string.ascii_letters + string.digits,
                                           k=random.randint(8, 100)))
    }
    return another_credentials


@pytest.fixture(scope="function")
def task_data() -> dict:
    task_data = {
        "name": "".join(random.choices(string.ascii_letters + string.digits,
                                       k=random.randint(1, 50))
                        ),
        "description": "".join(random.choices(string.ascii_letters + string.digits,
                                              k=random.randint(1, 300))
                               ),
        "status": False
    }
    return task_data


@pytest.fixture(scope="function")
async def access_token(test_client, credentials) -> str:
    """Register new user and return access-token for this user."""
    token_login = credentials["login"]
    token_password = credentials["password"]
    registered = await test_client.post("user/new",
                                        json={"login": token_login,
                                              "password": token_password,
                                              }
                                        )
    assert registered.status_code == 200
    response = await test_client.post("token",
                                      headers={"content-type": "application/x-www-form-urlencoded"},
                                      data={"username": token_login,
                                            "password": token_password,
                                            },
                                      )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token


@pytest.fixture(scope="function")
async def another_access_token(test_client, another_credentials) -> str:
    """Register new user and return access-token for this user."""
    token_login = another_credentials["login"]
    token_password = another_credentials["password"]
    registered = await test_client.post("user/new",
                                        json={"login": token_login,
                                              "password": token_password,
                                              }
                                        )
    assert registered.status_code == 200
    response = await test_client.post("token",
                                      headers={"content-type": "application/x-www-form-urlencoded"},
                                      data={"username": token_login,
                                            "password": token_password,
                                            },
                                      )
    assert response.status_code == 200
    another_token = response.json()["access_token"]
    return another_token


@pytest.fixture(scope="function")
async def admin_token(test_client) -> str:
    """Get admin access-token"""
    response = await test_client.post("token",
                                      headers={"content-type": "application/x-www-form-urlencoded"},
                                      data={"username": "admin",
                                            "password": "admin",
                                            },
                                      )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token
