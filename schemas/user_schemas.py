from pydantic import BaseModel, Field
from schemas.task_schemas import OneTaskResponse


class AccessToken(BaseModel):
    access_token: str = Field(
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                "eyJzdWIiOiJtYXJjdXMiLCJleHAiOjE2Nzk4MTY0OTN9."
                "9gvW7e7abYd_fmtNHnxbYfqPBMf66FjwmrPLHK3QckA",
        title="Created AccessToken",
    )
    token_type: str = Field(default="bearer",
                            title="Token type",
                            )
    user_id: int = Field(example=1,
                         title="User_id associated with a token",
                         )
    login: str = Field(example="Marcus",
                       title="Username associated with a token",
                       )


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
                       regex="^[A-Za-z\d]{2,}$",  # all letters, numbers, at least 2
                       )
    password: str = Field(example="Aurelius",
                          title="Preferred password",
                          min_length=8,
                          max_length=100,
                          regex="^[A-Za-z\d@$!%*#?&]{8,}$",  # all letters, numbers and special symbols, at least 8
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


class UpdateUser(BaseModel):
    new_login: str = Field(example="Mark",
                           title="New username",
                           min_length=2,
                           max_length=50,
                           regex="^[A-Za-z\d]{2,}$",
                           )
    new_password: str = Field(example="Maurelius",
                              title="New password",
                              min_length=8,
                              max_length=100,
                              regex="^[A-Za-z\d@$!%*#?&]{8,}$",
                              )


class UpdateUserResponse(BaseModel):
    id: int = Field(example=2,
                    title="Id of a user which data was updated",
                    )
    login: str = Field(example="Mark",
                       title="Updated username",
                       )

    class Config:
        orm_mode = True


class GetUser(BaseModel):
    id: int = Field(example=2,
                    title="Id of searched User",
                    )
    login: str = Field(example="Mark",
                       title="Login of searched user",
                       )
    user_tasks: list[OneTaskResponse] = Field(title="All Id associated Tasks")

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    login: str

    class Config:
        orm_mode = True


class GetAllUsers(BaseModel):
    __root__: list[User]
