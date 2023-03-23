from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import db_session
from schemas.schemas import CreateNewTask
from auth.oauth2 import oauth2_schema

task_router = APIRouter(prefix="/task",
                        tags=["task"],
                        )


@task_router.post("/new",
                  name="new task",
                  description="Add new task with given Name, Description",
                  )
async def add_new_task(task_data: CreateNewTask,
                       token: str = Depends(oauth2_schema),
                       db: Session = Depends(db_session),
                       ):
    return ...
