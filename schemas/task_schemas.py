from pydantic import BaseModel, Field


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
    task_id: int = Field(example=1,
                         title="Id of newly created task")
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


class UpdateTaskResponse(BaseModel):
    user_id: int = Field(example=1,
                         title="Active user ID",
                         )
    updated: int = Field(example=1,
                         title="Updated task ID")
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
                         title="Active user ID",
                         )
    user_tasks: list[OneTaskResponse]

    class Config:
        orm_mode = True
