from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database.database import db_session
from schemas.schemas import CreateNewUser, CreateNewUserResponse
from routers.register_func.functional import create_new_user


register_router = APIRouter(prefix="/register",
                            tags=["register"],
                            )


@register_router.post("/new",
                      name="New User",
                      response_model=CreateNewUserResponse,
                      description="Register new User with given credentials",
                      response_description="Successful response with Id and Login of registered User",
                      )
async def register_new_user(request: CreateNewUser,
                            db: Session = Depends(db_session),
                            ):
    return create_new_user(request, db)
