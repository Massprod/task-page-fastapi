from pydantic import BaseModel


class CreateNewUser(BaseModel):
    username: str = "Marcus"
    password: str = "Aurelius"


class CreateNewUserResponse(BaseModel):
    user_id: int = 1
    username: str = "Marcus"

    class Config:
        orm_mode = True

