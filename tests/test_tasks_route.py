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


@pytest.mark.asyncio
async def test_get_one_task_with_correct_token(access_token,
                                               database,
                                               task_data,
                                               test_client,
                                               ):
    """Test getting one task data with correct access-token for associated user_id"""
    test_token = await access_token
    test_user_id = get_current_user(token=test_token, db=database).id
    test_number = 3
    for x in range(test_number):
        test_data = task_data
        response = await test_client.post("task/new",
                                          json=test_data,
                                          headers={"Authorization": f"Bearer {test_token}"},
                                          )
        assert response.status_code == 200
        test_task_id = response.json()["task_id"]
        get_task = await test_client.get(f"task/{test_task_id}",
                                         headers={"Authorization": f"Bearer {test_token}"},
                                         )
        assert get_task.status_code == 200
        exist = database.query(DbTasks).filter_by(task_id=test_task_id).first()
        assert exist
        assert exist.user_id == test_user_id
    test_not_exist = 10002
    get_not_exist = await test_client.get(f"task/{test_not_exist}",
                                          headers={"Authorization": f"Bearer {test_token}"},
                                          )
    assert get_not_exist.status_code == 404
    not_exist = database.query(DbTasks).filter_by(task_id=test_not_exist).first()
    assert not_exist is None


@pytest.mark.asyncio
async def test_get_one_task_with_incorrect_token_and_empty_tasks(access_token,
                                                                 another_access_token,
                                                                 database,
                                                                 test_client,
                                                                 task_data,
                                                                 ):
    """
    Test getting one task data with incorrect access-token for associated user_id.
    Test getting one task data with correct access-token and 0 tasks created from associated user_id.
    """
    test_token = await another_access_token
    test_data = task_data
    response = await test_client.post("task/new",
                                      json=test_data,
                                      headers={"Authorization": f"Bearer {test_token}"},
                                      )
    assert response.status_code == 200
    test_task_id = response.json()["task_id"]
    exist = database.query(DbTasks).filter_by(task_id=test_task_id).first()
    assert exist
    test_incorrect_token = await access_token
    empty_call = await test_client.get(f"task/{test_task_id}",
                                       headers={"Authorization": f"Bearer {test_incorrect_token}"},
                                       )
    assert empty_call.status_code == 404
    response = await test_client.post("task/new",
                                      json=test_data,
                                      headers={"Authorization": f"Bearer {test_incorrect_token}"},
                                      )
    assert response.status_code == 200
    incorrect_call = await test_client.get(f"task/{test_task_id}",
                                           headers={"Authorization": f"Bearer {test_incorrect_token}"},
                                           )
    assert incorrect_call.status_code == 403
