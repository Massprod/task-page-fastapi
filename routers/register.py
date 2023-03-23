from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database.database import db_session
from schemas.schemas import CreateNewUser, CreateNewUserResponse
from routers.register_fun.functional import create_new_user


register_router = APIRouter(prefix="/register",
                            tags=["register"],
                            )


@register_router.post("/new",
                      name="Register New User",
                      response_model=CreateNewUserResponse,
                      description="Register new User with given credentials",
                      response_description="ID and Username for registered Entity"
                      )
async def register_new_user(user_data: CreateNewUser,
                            db: Session = Depends(db_session),
                            ):
    return create_new_user(user_data, db)
