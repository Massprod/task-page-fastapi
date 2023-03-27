from sqlalchemy.orm import Session
from database.models import DbTasks, DbUsers
from schemas.user_schemas import ActiveUser
from schemas.task_schemas import CreateNewTask, UpdateTask
from fastapi import HTTPException, status
from typing import Type


def validate_user_task(user: ActiveUser, task_id: int, db: Session):
    """Validate that chosen task created by Active user"""
    user_id = user.id
    validate_task = task_id
    user_tasks = db.query(DbUsers).filter_by(id=user_id).first().user_tasks
    if len(user_tasks) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: {user_id} don't have any created tasks",
                            )
    user_tasks_id = [_.task_id for _ in user_tasks]
    if validate_task not in user_tasks_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Task ID: {validate_task} not created by Active user id: {user_id}",
                            )
    return True


def create_task(user: ActiveUser, db: Session, request: CreateNewTask) -> DbTasks:
    """Create a new task record in DbTasks with given data."""
    name = request.name.strip()
    description = request.description.strip()
    task_status = request.status
    new_task = DbTasks(name=name,
                       description=description,
                       status=task_status,
                       user_id=user.id
                       )
    db.add(new_task)
    db.commit()
    return new_task


def get_all_tasks(user: ActiveUser, db: Session) -> list[Type[DbTasks] | None]:
    """Find all records in DbTasks for active user and return them."""
    user_id = user.id
    tasks = db.query(DbTasks).filter_by(user_id=user_id).all()
    return tasks


def get_task(user: ActiveUser, task_id: int, db: Session) -> Type[DbTasks] | None:
    """Find record in DbTasks with given task id. Returns found record."""
    task = db.query(DbTasks).filter_by(task_id=task_id).first()
    if task is None:
        return None
    validate_user_task(user=user, task_id=task_id, db=db)
    return task


def update_task(task_id: int, user: ActiveUser, db: Session, request: UpdateTask) -> Type[DbTasks] | bool:
    """Find record in DbTasks with given task_id. Update record with new data."""
    update_id = task_id
    new_name = request.name.strip()
    new_description = request.description.strip()
    new_status = request.status
    exist = db.query(DbTasks).filter_by(task_id=update_id).first()
    if not exist:
        return False   # can't use UPDATE on object given by .first()
    validate_user_task(user=user, task_id=update_id, db=db)
    db.query(DbTasks).filter_by(task_id=update_id).update({
        DbTasks.name: new_name,
        DbTasks.description: new_description,
        DbTasks.status: new_status,
    })
    db.commit()
    db.refresh(exist)
    return exist


def delete_task(user: ActiveUser, task_id: int, db: Session) -> bool:
    """Delete record from DbTasks with given task_id"""
    del_id = task_id
    task = get_task(user=user, task_id=del_id, db=db)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True


def delete_all_records(user: ActiveUser, db: Session) -> bool:
    user_id = user.id
    all_tasks = db.query(DbUsers).filter_by(id=user_id).first().user_tasks
    if len(all_tasks) == 0:
        return False
    for _ in all_tasks:
        db.delete(_)
    db.commit()
    return True
