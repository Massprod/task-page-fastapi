from sqlalchemy.orm import Session
from database.models import DbTasks
from typing import Type
from schemas.schemas import CreateNewTask, NewTaskResponse, ActiveUser, UpdateTask, AllTasksResponse, UpdateResponse
from database.crud.db_tasks import create_task, update_task, get_all_tasks
from fastapi import HTTPException, status


def create_new_task(user: ActiveUser, db: Session, request: CreateNewTask) -> NewTaskResponse:
    """Create a new Task record."""
    new_task = create_task(user=user, db=db, request=request)
    return new_task


def return_all_tasks(current_user: ActiveUser, db: Session) -> AllTasksResponse:
    user_tasks = get_all_tasks(user=current_user, db=db)
    return AllTasksResponse(user_id=current_user.id,
                            user_tasks=user_tasks,
                            )


def update_existing_task(user: ActiveUser, request: UpdateTask, db: Session) -> UpdateResponse:
    updated = update_task(db=db, request=request)
    if updated:
        return UpdateResponse(user_id=user.id,
                              updated=True,
                              name=updated.name,
                              description=updated.description,
                              status=updated.status,
                              )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Task with ID: {request.task_id} not found.",
                        )
