from pydantic import BaseModel, Field


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
                          max_length=50,
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
                      )
    description: str = Field(example="always calm",
                             title="Description of a task",
                             )
    status: bool = Field(default=False,
                         title="Status of a task",
                         )


class ResponseNewTask(BaseModel):
    user_id: int = Field(example=1,
                         title="Id of called user",
                         )
    added: bool = True
    name: str = Field(example="stay calm",
                      title="Name of a new Task",
                      )
    description: str = Field(example="always calm",
                             title="Description of a new task",
                             )

    class Config:
        orm_mode = True


class UpdateTask(BaseModel):
    name: str | None = Field(default=None,
                             title="New task name",
                             )
    description: str | None = Field(default=None,
                                    title="New task description",
                                    )
    status: bool | None = Field(default=None,
                                title="New task status",
                                )
