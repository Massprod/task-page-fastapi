from sqlalchemy.orm import Session
from database.models import DbTasks
from schemas.schemas import CreateNewTask, UpdateTask, ActiveUser
from typing import Type


def create_task(user: ActiveUser, db: Session, request: CreateNewTask) -> DbTasks:
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


def get_all_tasks(user: ActiveUser, db: Session) -> list[Type[DbTasks] | None]:
    """Find all records in DbTasks for active user and return them."""
    user_id = user.id
    tasks = db.query(DbTasks).filter_by(id=user_id).all()
    return tasks


def get_task(task_id: int, db: Session) -> Type[DbTasks] | None:
    """Find record in DbTasks with given task id. Returns found record."""
    task = db.query(DbTasks).filter_by(task_id=task_id).first()
    return task


def update_task(task_id: int, db: Session, request: UpdateTask) -> bool:
    """Find record in DbTasks with given task_id. Update record with new data."""
    update_entity = {}
    if new_name := request.name is not None:
        update_entity[DbTasks.name] = new_name
    if new_description := request.description is not None:
        update_entity[DbTasks.description] = new_description
    if new_status := request.status is not None:
        update_entity[DbTasks.status] = new_status
    exist = get_task(task_id=task_id, db=db)
    if exist is None:
        return False
    exist.update(update_entity)
    db.commit()
    return True


def delete_task(task_id: int, db: Session) -> bool:
    """Delete record from DbTasks with given task_id"""
    del_id = task_id
    task = get_task(task_id=del_id, db=db)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True
