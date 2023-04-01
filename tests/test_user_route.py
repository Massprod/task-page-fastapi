import pytest
from database.models import DbUsers
from database.hash import Hash
from auth.oauth2 import get_current_user


@pytest.mark.asyncio
async def test_create_new_user_and_duplicate(test_client, database, credentials):
    """
    Test creating of a new user with correct credentials.
    Test creating of a new user with already existing Login.
    """
    test_login = credentials["login"]
    test_password = credentials["password"]
    response = await test_client.post("user/new",
                                      json={"login": test_login,
                                            "password": test_password,
                                            }
                                      )
    assert response.status_code == 200
    response = await test_client.post("user/new",
                                      json={"login": test_login,
                                            "password": test_password,
                                            }
                                      )
    assert response.status_code == 403
    exist = database.query(DbUsers).filter_by(login=test_login).first()
    assert exist
    verify = Hash().verify_pass(exist.password, test_password)
    assert verify


@pytest.mark.asyncio
async def test_update_user_credentials_with_correct_token(database,
                                                          test_client,
                                                          access_token,
                                                          credentials
                                                          ):
    """Test updating existing user data with correct access-token for given id"""
    test_login = credentials["login"]
    test_password = credentials["password"]
    test_token = await access_token
    test_user_id = get_current_user(token=test_token, db=database).id
    response = await test_client.put(f"user/{test_user_id}",
                                     headers={"Authorization": f"Bearer {test_token}"},
                                     json={"new_login": test_login,
                                           "new_password": test_password,
                                           }
                                     )
    assert response.status_code == 200
    exist = database.query(DbUsers).filter_by(login=test_login).first()
    assert exist
    assert exist.id == test_user_id


@pytest.mark.asyncio
async def test_update_user_with_incorrect_token(database,
                                                test_client,
                                                access_token,
                                                credentials,
                                                ):
    """Test updating existing user with incorrect access-token for given id"""
    test_login = credentials["login"]
    test_password = credentials["password"]
    test_token = await access_token
    test_user_id = 10002
    response = await test_client.put(f"user/{test_user_id}",
                                     headers={"Authorization": f"Bearer {test_token}"},
                                     json={"new_login": test_login,
                                           "new_password": test_password,
                                           }
                                     )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_user_with_admin_access(database,
                                             test_client,
                                             admin_token,
                                             credentials
                                             ):
    """Test updating with admin access-token"""
    test_login = credentials["login"]
    test_password = credentials["password"]
    test_new_login = "admininterference"
    test_new_password = "admininterference"
    test_admin_token = await admin_token
    not_registered_id = 10002
    response = await test_client.post("user/new",
                                      json={"login": test_login,
                                            "password": test_password,
                                            }
                                      )
    assert response.status_code == 200
    exist = database.query(DbUsers).filter_by(login=test_login).first()
    assert exist
    new_id = exist.id
    update = await test_client.put(f"user/{new_id}",
                                   headers={"Authorization": f"Bearer {test_admin_token}"},
                                   json={"new_login": test_new_login,
                                         "new_password": test_new_password,
                                         }
                                   )
    assert update.status_code == 200
    exist = database.query(DbUsers).filter_by(login=test_new_login).first()
    assert exist
    not_exist = await test_client.put(f"user/{not_registered_id}",
                                      headers={"Authorization": f"Bearer {test_admin_token}"},
                                      json={"new_login": test_new_login,
                                            "new_password": test_new_password,
                                            }
                                      )
    assert not_exist.status_code == 404
    admin_change = await test_client.put("user/1",
                                         headers={"Authorization": f"Bearer {test_admin_token}"},
                                         json={"new_login": test_new_login,
                                               "new_password": test_new_password,
                                               }
                                         )
    assert admin_change.status_code == 403


@pytest.mark.asyncio
async def test_delete_user_with_correct_token(test_client,
                                              database,
                                              access_token,
                                              ):
    """Test delete existing user data with correct access-token for given id"""
    test_token = await access_token
    test_id = get_current_user(token=test_token, db=database).id
    response = await test_client.delete(f"user/{test_id}",
                                        headers={"Authorization": f"Bearer {test_token}"},
                                        )
    assert response.status_code == 204
    exist = database.query(DbUsers).filter_by(id=test_id).first()
    assert exist is None


@pytest.mark.asyncio
async def test_delete_user_with_admin_access(test_client,
                                             database,
                                             admin_token,
                                             credentials,
                                             ):
    """Test deleting with admin access-token"""
    test_login = credentials["login"]
    test_password = credentials["password"]
    test_admin_token = await admin_token
    not_registered_id = 10002
    response = await test_client.post("user/new",
                                      json={"login": test_login,
                                            "password": test_password,
                                            }
                                      )
    assert response.status_code == 200
    new_id = response.json()["id"]
    delete = await test_client.delete(f"user/{new_id}",
                                      headers={"Authorization": f"Bearer {test_admin_token}"},
                                      )
    assert delete.status_code == 204
    exist = database.query(DbUsers).filter_by(login=test_login).first()
    assert exist is None
    not_existing = await test_client.delete(f"user/{not_registered_id}",
                                            headers={"Authorization": f"Bearer {test_admin_token}",
                                                     }
                                            )
    assert not_existing.status_code == 404
    admin_delete = await test_client.delete(f"user/1",
                                            headers={"Authorization": f"Bearer {test_admin_token}",
                                                     }
                                            )
    assert admin_delete.status_code == 403


@pytest.mark.asyncio
async def test_get_user_with_correct_token(access_token,
                                           database,
                                           test_client,
                                           ):
    """Test getting user data with correct access-token"""
    test_token = await access_token
    test_id = get_current_user(token=test_token, db=database).id
    response = await test_client.get(f"user/{test_id}",
                                     headers={"Authorization": f"Bearer {test_token}",
                                              }
                                     )
    assert response.status_code == 200
    exist = database.query(DbUsers).filter_by(id=test_id).first()
    assert exist


@pytest.mark.asyncio
async def test_get_user_with_incorrect_token(access_token,
                                             database,
                                             test_client,
                                             ):
    """Test getting other users data with correct access-token"""
    test_token = await access_token
    test_id = 10002
    response = await test_client.get(f"user/{test_id}",
                                     headers={"Authorization": f"Bearer {test_token}",
                                              }
                                     )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_user_with_admin_token(admin_token,
                                         database,
                                         test_client,
                                         access_token,
                                         ):
    """Test getting any user data with admin access-token"""
    test_token = await access_token
    test_id = get_current_user(token=test_token, db=database).id
    test_admin_token = await admin_token
    not_exist_id = 10002
    response = await test_client.get(f"user/{test_id}",
                                     headers={"Authorization": f"Bearer {test_admin_token}",
                                              }
                                     )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == test_id
    exist = database.query(DbUsers).filter_by(id=response_data["id"]).first()
    assert exist
    admin_call = await test_client.get(f"user/1",
                                       headers={"Authorization": f"Bearer {test_admin_token}",
                                                }
                                       )
    assert admin_call.status_code == 200
    not_exist_id_call = await test_client.get(f"user/{not_exist_id}",
                                              headers={"Authorization": f"Bearer {test_admin_token}",
                                                       }
                                              )
    assert not_exist_id_call.status_code == 404
    not_exist = database.query(DbUsers).filter_by(id=not_exist_id).first()
    assert not_exist is None


@pytest.mark.asyncio
async def test_get_all_users_with_admin_token(admin_token,
                                              test_client,
                                              ):
    """Test getting all users data with admin access-token"""
    test_admin_token = await admin_token
    response = await test_client.get(f"user/all",
                                     headers={"Authorization": f"Bearer {test_admin_token}",
                                              }
                                     )
    assert response.status_code == 200
    assert type(response.json()) is list


@pytest.mark.asyncio
async def test_get_all_users_with_incorrect_access_token(access_token,
                                                         test_client,
                                                         ):
    """Test getting all users data with any not admin access-token"""
    test_token = await access_token
    response = await test_client.get(f"user/all",
                                     headers={"Authorization": f"Bearer {test_token}",
                                              }
                                     )
    assert response.status_code == 403
