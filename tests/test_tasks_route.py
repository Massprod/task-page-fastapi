import pytest
from database.models import DbTasks
from auth.oauth2 import get_current_user


@pytest.mark.asyncio
async def test_create_new_task(access_token,
                               database,
                               task_data,
                               test_client,
                               ):
    """Test creating a new task with correct access-token"""
    test_data = task_data
    test_token = await access_token
    test_user_id = get_current_user(token=test_token, db=database).id
    response = await test_client.post("task/new",
                                      json=test_data,
                                      headers={"Authorization": f"Bearer {test_token}"},
                                      )
    assert response.status_code == 200
    exist = database.query(DbTasks).filter_by(name=test_data["name"]).first()
    assert exist
    assert exist.user_id == test_user_id


@pytest.mark.asyncio
async def test_get_all_tasks(access_token,
                             database,
                             task_data,
                             test_client,
                             ):
    """Test getting all tasks data with correct access-token for associated user_id"""
    test_token = await access_token
    test_user_id = get_current_user(token=test_token, db=database).id
    test_number = 5
    for x in range(test_number):
        test_data = task_data
        response = await test_client.post("task/new",
                                          json=test_data,
                                          headers={"Authorization": f"Bearer {test_token}"},
                                          )
        assert response.status_code == 200
        exist = database.query(DbTasks).filter_by(name=test_data["name"]).first()
        assert exist
        assert exist.user_id == test_user_id
    response = await test_client.get("task/all",
                                     headers={"Authorization": f"Bearer {test_token}"},
                                     )
    assert response.status_code == 200
    response_id = response.json()["user_id"]
    assert response_id == test_user_id
    response_tasks = len(response.json()["user_tasks"])
    assert response_tasks == test_number
