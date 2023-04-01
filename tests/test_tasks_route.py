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


@pytest.mark.asyncio
async def test_delete_all_tasks(database,
                                task_data,
                                access_token,
                                test_client,
                                ):
    """
    Test deleting all tasks associated with access-token user_id.
    Test deleting all tasks associated with access-token user_id if user don't have any task records.
    """
    test_token = await access_token
    test_data = task_data
    test_number = 4
    for x in range(test_number):
        response = await test_client.post("task/new",
                                          json=test_data,
                                          headers={"Authorization": f"Bearer {test_token}"},
                                          )
        assert response.status_code == 200
        test_task_id = response.json()["task_id"]
        exist = database.query(DbTasks).filter_by(task_id=test_task_id).first()
        assert exist
    delete_all_exist = await test_client.delete("task/all",
                                                headers={"Authorization": f"Bearer {test_token}"},
                                                )
    assert delete_all_exist.status_code == 204
    delete_all_not_exist = await test_client.delete("task/all",
                                                    headers={"Authorization": f"Bearer {test_token}"},
                                                    )
    assert delete_all_not_exist.status_code == 404


@pytest.mark.asyncio
async def test_update_task(database,
                           task_data,
                           access_token,
                           test_client,
                           ):
    """
    Test updating existing task records associated with active user_id and access-token.
    Test trying to update not existing records with active user_id and access-token.
    """
    test_token = await access_token
    test_data = task_data
    test_new_data = {"name": "updated_name",
                     "description": "updated_description1",
                     "status": True,
                     }
    test_not_exist = 10002
    response = await test_client.post("task/new",
                                      json=test_data,
                                      headers={"Authorization": f"Bearer {test_token}"},
                                      )
    assert response.status_code == 200
    test_task_id = response.json()["task_id"]
    exist = database.query(DbTasks).filter_by(name=test_data["name"]).first()
    assert exist
    update_correct = await test_client.put(f"task/{test_task_id}",
                                           json=test_new_data,
                                           headers={"Authorization": f"Bearer {test_token}"},
                                           )
    assert update_correct.status_code == 200
    update_exist = database.query(DbTasks).filter_by(name=test_new_data["name"]).first()
    database.refresh(update_exist)
    assert update_exist
    assert update_exist.status is True
    not_exist = await test_client.put(f"task/{test_not_exist}",
                                      json=test_new_data,
                                      headers={"Authorization": f"Bearer {test_token}"},
                                      )
    assert not_exist.status_code == 404


@pytest.mark.asyncio
async def test_delete_one_task(access_token,
                               database,
                               task_data,
                               test_client,
                               ):
    """
    Test deleting one task created by active user with access-token.
    Test trying to delete not existing task with correct access-token.
    """
    test_token = await access_token
    test_data = task_data
    response = await test_client.post("task/new",
                                      json=test_data,
                                      headers={"Authorization": f"Bearer {test_token}"},
                                      )
    assert response.status_code == 200
    exist = database.query(DbTasks).filter_by(name=test_data["name"]).first()
    assert exist
    test_task_id = exist.task_id
    delete_correct = await test_client.delete(f"task/{test_task_id}",
                                              headers={"Authorization": f"Bearer {test_token}"},
                                              )
    assert delete_correct.status_code == 204
    exist = database.query(DbTasks).filter_by(name=test_data["name"]).first()
    assert exist is None
    delete_incorrect = await test_client.delete(f"task/{test_task_id}",
                                                headers={"Authorization": f"Bearer {test_token}"},
                                                )
    assert delete_incorrect.status_code == 404


@pytest.mark.asyncio
async def test_get_delete_update_with_admin_token(admin_token,
                                                  access_token,
                                                  task_data,
                                                  test_client,
                                                  database,
                                                  ):
    """
    Test get, update, delete tasks with admin access-token.
    """
    test_admin_token = await admin_token
    test_token = await access_token
    test_data = task_data
    test_new_data = {"name": "updated_name_by_admin",
                     "description": "updated_description1_by_admin",
                     "status": True,
                     }
    response = await test_client.post("task/new",
                                      json=test_data,
                                      headers={"Authorization": f"Bearer {test_token}"},
                                      )
    assert response.status_code == 200
    exist = database.query(DbTasks).filter_by(name=test_data["name"]).first()
    assert exist
    test_task_id = exist.task_id
    update_task = await test_client.put(f"task/{test_task_id}",
                                        json=test_new_data,
                                        headers={"Authorization": f"Bearer {test_admin_token}"},
                                        )
    assert update_task.status_code == 200
    database.refresh(exist)
    assert exist.name == test_new_data["name"]
    get_task = await test_client.get(f"task/{test_task_id}",
                                     headers={"Authorization": f"Bearer {test_admin_token}"},
                                     )
    assert get_task.status_code == 200
    delete_task = await test_client.delete(f"task/{test_task_id}",
                                           headers={"Authorization": f"Bearer {test_admin_token}"},
                                           )
    assert delete_task.status_code == 204
