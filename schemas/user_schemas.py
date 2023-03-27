from pydantic import BaseModel, Field


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


class UpdateUser(BaseModel):
    new_login: str = Field(example="Mark",
                           title="New username",
                           min_length=2,
                           max_length=50,
                           )
    new_password: str = Field(example="Maurelius",
                              title="New password",
                              min_length=8,
                              max_length=100,
                              )
