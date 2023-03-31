import pytest
from database.models import DbUsers
from auth.oauth2 import create_access_token, get_current_user
from fastapi import HTTPException
from jose.exceptions import JWTError


@pytest.mark.asyncio
async def test_create_new_token_correct_credentials(test_client, database, credentials):
    """Test creating of a new access-token with correct credentials and existing user"""
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
async def test_get_new_token_incorrect_credentials(test_client, database, credentials):
    """Test creating of a new access-token with incorrect credentials and existing user"""
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


@pytest.mark.asyncio
async def test_get_current_user_with_incorrect_token_data(database):
    """Test function for getting active-user with incorrect token data"""
    test_data = {"subb": "testSubb"}
    test_token = create_access_token(data=test_data)
    with pytest.raises(HTTPException):
        get_current_user(token=test_token, db=database)


@pytest.mark.asyncio
async def test_get_current_user_jwt_exception_with_correct_token_data(mocker, database, access_token):
    """
    Test function for getting active-user with correct token data,
    but raised JWT exception by jwt_decode
    """
    test_token = await access_token
    mocker.patch("auth.oauth2.jwt.decode", side_effect=JWTError)
    with pytest.raises(HTTPException):
        get_current_user(token=test_token, db=database)


@pytest.mark.asyncio
async def test_get_current_user_with_not_existing_user_data(database):
    """
    Test function for getting active-user with correct token,
    but unregistered user data
    """
    test_data = {"sub": "testSubb"}
    test_token = create_access_token(data=test_data)
    with pytest.raises(HTTPException):
        get_current_user(token=test_token, db=database)
