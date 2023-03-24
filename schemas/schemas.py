from pydantic import BaseModel, Field


class CreateNewUser(BaseModel):
    login: str = Field(example="Marcus",
                       title="Preferred username",
                       min_length=2,
                       max_length=50,
                       )
    password: str = Field(example="Aurelius",
                          title="Preferred password",
                          min_length=8,
                          max_length=50,
                          )


class CreateNewUserResponse(BaseModel):
    user_id: int = Field(example=1,
                         title="user id",
                         )
    login: str = Field(example="marcus",
                       title="Registered username",
                       )

    class Config:
        orm_mode = True


class CreateNewTask(BaseModel):
    name: str = Field(title="Name of a task")
    description: str = Field(title="Description of a task")
