from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import db_session
from schemas.schemas import CreateNewTask, ActiveUser, ResponseNewTask, UpdateTask, UpdateResponse
from auth.oauth2 import get_current_user
from routers.task_func.functional import create_new_task, update_exist_task

task_router = APIRouter(prefix="/task",
                        tags=["task"],
                        )


@task_router.post("/new",
                  name="new task",
                  response_model=ResponseNewTask,
                  description="Create new task with given Name, Description",
                  response_description="Successful response with user Id and created Task data"
                  )
async def add_new_task(request: CreateNewTask,
                       current_user: ActiveUser = Depends(get_current_user),
                       db: Session = Depends(db_session),
                       ):
    return create_new_task(user=current_user, db=db, request=request)


@task_router.post("/update",
                  name="update task",
                  response_model=UpdateResponse,
                  )
async def update_task_by_id(request: UpdateTask,
                            current_user: ActiveUser = Depends(get_current_user),
                            db: Session = Depends(db_session),
                            ):
    return update_exist_task(request=request, db=db)
