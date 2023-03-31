import pytest
from database.models import DbUsers
from database.hash import Hash


@pytest.mark.asyncio
async def test_create_new_user_and_duplicate(test_client, database, credentials):
    """Test creating of a new user with correct credentials and duplicating already existing"""
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


# @pytest.mark.asyncio
# async def test_create_new_user_not_correct_credentials(credentials):
#     """Test creating of a new user with incorrect credentials"""
#     pass

