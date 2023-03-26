from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database.database import db_session
from schemas.schemas import CreateNewTask, ActiveUser, NewTaskResponse
from schemas.schemas import UpdateTask, UpdateResponse, AllTasksResponse, OneTaskResponse
from auth.oauth2 import get_current_user
from routers.task_func.functional import create_new_task, update_existing_task, return_all_tasks, return_one_task

task_router = APIRouter(prefix="/task",
                        tags=["task"],
                        )


@task_router.post("/new",
                  name="new task",
                  response_model=NewTaskResponse,
                  description="Create new task with given Name, Description",
                  response_description="Successful response with user Id and created Task data"
                  )
async def add_new_task(request: CreateNewTask,
                       current_user: ActiveUser = Depends(get_current_user),
                       db: Session = Depends(db_session),
                       ):
    return create_new_task(user=current_user, db=db, request=request)


@task_router.get("/{task_id}",
                 name="Get task",
                 response_model=OneTaskResponse,
                 )
def get_one_task(task_id: int = Path(...),
                 db: Session = Depends(db_session),
                 current_user: ActiveUser = Depends(get_current_user),
                 ):
    return return_one_task(user=current_user, task_id=task_id, db=db)


@task_router.get("/all",
                 name="Get all tasks",
                 response_model=AllTasksResponse,
                 description="Returns all tasks for currently Active user",
                 response_description="Successful response with all Task for user ID"
                 )
async def get_all_tasks(current_user: ActiveUser = Depends(get_current_user),
                        db: Session = Depends(db_session),
                        ):
    return return_all_tasks(current_user=current_user, db=db)


@task_router.put("/update",
                 name="update task",
                 response_model=UpdateResponse,
                 description="Updating already existing task with new Data",
                 response_description="Successful response with Updated task data"
                 )
async def update_task_by_id(request: UpdateTask,
                            current_user: ActiveUser = Depends(get_current_user),
                            db: Session = Depends(db_session),
                            ):
    return update_existing_task(user=current_user, request=request, db=db)
