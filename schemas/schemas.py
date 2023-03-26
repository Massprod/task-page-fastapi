from pydantic import BaseModel, Field
from typing import Type
from database.models import DbTasks


class AccessToken(BaseModel):
    access_token: str = Field(
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjdXMiLCJleHAiOjE2Nzk4MTY0OTN9.9gvW7e7abYd_fmtNHnxbYfqPBMf66FjwmrPLHK3QckA",
        title="Created AccessToken",
    )
    token_type: str = Field(default="bearer",
                            title="Token type",
                            )
    user_id: int = Field(example=1,
                         title="User_id associated with a token",
                         )
    login: str = Field(example="Marcus",
                       title="Username associated with a token")


class ActiveUser(BaseModel):
    id: int = Field(example=1,
                    title="Authenticated user Id",
                    )
    login: str = Field(example="Marcus",
                       title="Authenticated user Username",
                       )

    class Config:
        orm_mode = True


class CreateNewUser(BaseModel):
    login: str = Field(example="Marcus",
                       title="Preferred username",
                       min_length=2,
                       max_length=50,
                       )
    password: str = Field(example="Aurelius",
                          title="Preferred password",
                          min_length=8,
                          max_length=100,
                          )


class CreateNewUserResponse(BaseModel):
    id: int = Field(example=1,
                    title="user id",
                    )
    login: str = Field(example="marcus",
                       title="Registered username",
                       )

    class Config:
        orm_mode = True


class CreateNewTask(BaseModel):
    name: str = Field(example="stay calm",
                      title="Name of a task",
                      min_length=1,
                      max_length=50,
                      )
    description: str = Field(example="always calm",
                             title="Description of a task",
                             min_length=1,
                             max_length=300,
                             )
    status: bool = Field(default=False,
                         title="Status of a task",
                         )


class NewTaskResponse(BaseModel):
    user_id: int = Field(example=1,
                         title="ID of called user",
                         )
    added: bool = True
    name: str = Field(example="stay calm",
                      title="Name of a new Task",
                      min_length=1,
                      max_length=50,
                      )
    description: str = Field(example="always calm",
                             title="Description of a new task",
                             min_length=1,
                             max_length=300,
                             )

    class Config:
        orm_mode = True


class UpdateTask(BaseModel):
    task_id: int = Field(example=1,
                         title="ID of chosen Task",
                         )
    name: str = Field(example="New Name here",
                      title="New task name",
                      min_length=1,
                      max_length=50,
                      )
    description: str = Field(example="New description here",
                             title="New description",
                             min_length=1,
                             max_length=300,
                             )
    status: bool = Field(example=True,
                         title="New task status",
                         )

    class Config:
        orm_mode = True


class UpdateResponse(BaseModel):
    user_id: int = Field(example=1,
                         title="Active user ID",
                         )
    updated: bool = True
    name: str = Field(example="stay close",
                      title="Updated name",
                      min_length=1,
                      max_length=50,
                      )
    description: str = Field(example="stay closer",
                             title="Updated description",
                             min_length=1,
                             max_length=300,
                             )
    status: bool = Field(example=True,
                         title="Updated status",
                         )

    class Config:
        orm_mode = True


class OneTaskResponse(BaseModel):
    task_id: int = Field(example=1,
                         title="ID of chosen Task",
                         )
    name: str = Field(example="New Name here",
                      title="New task name",
                      min_length=1,
                      max_length=50,
                      )
    description: str = Field(example="New description here",
                             title="New description",
                             min_length=1,
                             max_length=300,
                             )
    status: bool = Field(example=True,
                         title="New task status",
                         )

    class Config:
        orm_mode = True


class AllTasksResponse(BaseModel):
    user_id: int = Field(example=1,
                         title="Active user ID")
    user_tasks: list[OneTaskResponse]

    class Config:
        orm_mode = True
