from sqlalchemy.orm import Session
from database.models import DbUsers
from schemas.schemas import CreateNewTask, ResponseNewTask, ActiveUser, UpdateTask, UpdateResponse
from database.crud.db_tasks import create_task, update_task
from fastapi import HTTPException, status


def create_new_task(user: ActiveUser, db: Session, request: CreateNewTask) -> ResponseNewTask:
    """Create a new Task record."""
    new_task = create_task(user=user, db=db, request=request)
    return new_task


def update_exist_task(request: UpdateTask, db: Session):
    updated = update_task(db=db, request=request)
    if updated:
        return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Task with ID: {request.task_id} not found.",
                        )
