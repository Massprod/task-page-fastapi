from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import db_session
from schemas.schemas import CreateNewTask, ActiveUser, ResponseNewTask
from auth.oauth2 import get_current_user
from routers.task_func.functional import create_new_task

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
