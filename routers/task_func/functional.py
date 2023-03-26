from sqlalchemy.orm import Session
from schemas.schemas import CreateNewTask, ResponseNewTask, ActiveUser
from database.crud.db_tasks import create_task


def create_new_task(user: ActiveUser, db: Session, request: CreateNewTask) -> ResponseNewTask:
    """Create a new Task record."""
    new_task = create_task(user=user, db=db, request=request)
    return new_task
