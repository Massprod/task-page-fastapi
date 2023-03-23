from pydantic import BaseModel, Field


class CreateNewUser(BaseModel):
    username: str = Field(default="Marcus",
                          title="Preferred username",
                          min_length=2,
                          max_length=50,
                          )
    password: str = Field(default="Aurelius",
                          title="Preferred password",
                          min_length=8,
                          max_length=50,
                          )


class CreateNewUserResponse(BaseModel):
    user_id: int = Field(default=1,
                         title="user id",
                         )
    username: str = Field(default="Marcus",
                          title="Registered username",
                          )

    class Config:
        orm_mode = True

