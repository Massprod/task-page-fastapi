from sqlalchemy.orm import Session
from database.models import DbTasks
from schemas.schemas import CreateNewTask, CreateNewUserResponse


def create_task(user: CreateNewUserResponse, db: Session, request: CreateNewTask) -> DbTasks:
    """Create a new task record in DbTasks with given data."""
    name = request.name.strip()
    description = request.description.strip()
    status = request.status
    new_task = DbTasks(name=name,
                       description=description,
                       status=status,
                       user_id=user.id
                       )
    db.add(new_task)
    db.commit()
    return new_task
