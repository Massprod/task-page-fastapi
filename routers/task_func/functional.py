from sqlalchemy.orm import Session
from schemas.user_schemas import ActiveUser
from schemas.task_schemas import CreateNewTask, NewTaskResponse, UpdateTask
from schemas.task_schemas import AllTasksResponse, UpdateTaskResponse, OneTaskResponse
from database.crud.db_tasks import create_task, update_task, get_all_tasks, get_task, delete_task, delete_all_records
from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse


def create_new_task(user: ActiveUser, db: Session, request: CreateNewTask) -> NewTaskResponse:
    """Create a new Task record for Active user"""
    new_task = create_task(user=user, db=db, request=request)
    return new_task


def return_all_tasks(current_user: ActiveUser, db: Session) -> AllTasksResponse:
    """Return all existing task records for Active user"""
    user_tasks = get_all_tasks(user=current_user, db=db)
    return AllTasksResponse(user_id=current_user.id,
                            user_tasks=user_tasks,
                            )


def return_one_task(user: ActiveUser, task_id: int, db: Session) -> OneTaskResponse:
    """Return task for given ID, if it's exist and created by Active user"""
    task = get_task(user=user, task_id=task_id, db=db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with ID: {task_id} not found.")
    return OneTaskResponse(task_id=task.task_id,
                           name=task.name,
                           description=task.description,
                           status=task.status,
                           )


def update_existing_task(user: ActiveUser, task_id: int, request: UpdateTask, db: Session) -> UpdateTaskResponse:
    """Update and return updated Task info, if it's exist and created by Active user"""
    user_id = user.id
    updated = update_task(task_id=task_id, user=user, db=db, request=request)
    if updated:
        return UpdateTaskResponse(user_id=user_id,
                                  updated=task_id,
                                  name=updated.name,
                                  description=updated.description,
                                  status=updated.status,
                                  )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Task with ID: {task_id} not found.",
                        )


def delete_one_task(user: ActiveUser, task_id: int, db: Session) -> HTMLResponse:
    """Delete one task record, if it's exist and created by Active user"""
    deleted = delete_task(user=user, task_id=task_id, db=db)
    if deleted:
        return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Task with ID: {task_id} not found",
                        )


def delete_all_tasks(user: ActiveUser, db: Session) -> HTMLResponse:
    """Delete all task records created by Active user"""
    deleted = delete_all_records(user=user, db=db)
    if deleted:
        return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No records for user_id: {user.id}",
                        )
