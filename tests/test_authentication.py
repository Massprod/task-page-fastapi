import pytest
from database.models import DbUsers


@pytest.mark.asyncio
async def test_create_new_token_correct_credentials(test_client, database, credentials):
    test_login = credentials["login"]
    test_password = credentials["password"]
    registered = await test_client.post("user/new",
                                        json={"login": test_login,
                                              "password": test_password,
                                              }
                                        )
    assert registered.status_code == 200
    response = await test_client.post("token",
                                      headers={"content-type": "application/x-www-form-urlencoded"},
                                      data={"username": test_login,
                                            "password": test_password,
                                            },
                                      )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_new_token_incorrect_credentials(test_client, database, credentials):
    """Test creating of a new user and getting a token"""
    test_login = credentials["login"]
    test_password = credentials["password"]
    exist = database.query(DbUsers).filter_by(login=test_login).first()
    response = await test_client.post("user/new",
                                      json={"login": test_login,
                                            "password": test_password,
                                            }
                                      )
    assert response.status_code == 200
    exist = database.query(DbUsers).filter_by(login=test_login).first()
    assert exist
    incorrect_login = await test_client.post("token",
                                             headers={"content-type": "application/x-www-form-urlencoded"},
                                             data={"username": "notCorrectUsername",
                                                   "password": test_password,
                                                   }
                                             )
    assert incorrect_login.status_code == 404
    incorrect_password = await test_client.post("token",
                                                headers={"content-type": "application/x-www-form-urlencoded"},
                                                data={"username": test_login,
                                                      "password": "incorrectPassword123",
                                                      }
                                                )
    assert incorrect_password.status_code == 403
