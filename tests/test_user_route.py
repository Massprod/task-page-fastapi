import pytest
from sqlalchemy.orm import Session
from conf_test_db import app, override_db_session
from httpx import AsyncClient
import random
import string
from database.models import DbUsers
from database.hash import Hash


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://test/"


@pytest.fixture(scope="session")
def test_client(base_url) -> AsyncClient:
    return AsyncClient(app=app, base_url=base_url)


@pytest.fixture(scope="function")
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


@pytest.mark.asyncio
async def test_create_new_user(test_client, database, credentials):
    """Test creating of a new user with correct credentials"""
    test_login = credentials["login"]
    test_password = credentials["password"]
    response = await test_client.post("user/new",
                                      json={"login": test_login,
                                            "password": test_password,
                                            }
                                      )
    assert response.status_code == 200
    exist = database.query(DbUsers).filter_by(login=test_login).first()
    assert exist
    verify = Hash().verify_pass(exist.password, test_password)
    assert verify
