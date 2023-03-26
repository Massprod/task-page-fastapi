from sqlalchemy.orm import Session
from database.models import DbTasks, DbUsers
from typing import Type
from schemas.schemas import CreateNewTask, NewTaskResponse, ActiveUser, UpdateTask
from schemas.schemas import AllTasksResponse, UpdateResponse, OneTaskResponse
from database.crud.db_tasks import create_task, update_task, get_all_tasks, get_task, validate_user_task
from fastapi import HTTPException, status


def create_new_task(user: ActiveUser, db: Session, request: CreateNewTask) -> NewTaskResponse:
    """Create a new Task record."""
    new_task = create_task(user=user, db=db, request=request)
    return new_task


def return_all_tasks(current_user: ActiveUser, db: Session) -> AllTasksResponse:
    """Return all task records for Active user ID"""
    user_tasks = get_all_tasks(user=current_user, db=db)
    return AllTasksResponse(user_id=current_user.id,
                            user_tasks=user_tasks,
                            )


def return_one_task(user: ActiveUser, task_id: int, db: Session) -> OneTaskResponse:
    """Return task for given ID"""
    task = get_task(user=user, task_id=task_id, db=db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with ID: {task_id} not found.")
    return OneTaskResponse(task_id=task.task_id,
                           name=task.name,
                           description=task.description,
                           status=task.status,
                           )


def update_existing_task(user: ActiveUser, request: UpdateTask, db: Session) -> UpdateResponse:
    """Update and return updated Task info for """
    user_id = user.id
    updated = update_task(user=user, db=db, request=request)
    if updated:
        return UpdateResponse(user_id=user_id,
                              updated=True,
                              name=updated.name,
                              description=updated.description,
                              status=updated.status,
                              )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Task with ID: {request.task_id} not found.",
                        )
