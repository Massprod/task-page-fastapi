from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import db_session
from schemas.schemas import CreateNewTask, CreateNewUserResponse
from auth.oauth2 import get_current_user

task_router = APIRouter(prefix="/task",
                        tags=["task"],
                        )


@task_router.post("/new",
                  name="new task",
                  description="Add new task with given Name, Description",
                  )
async def add_new_task(task_data: CreateNewTask,
                       current_user: CreateNewUserResponse = Depends(get_current_user),
                       db: Session = Depends(db_session),
                       ):
    return {"test": "test",
            "current_user": current_user,
            }
