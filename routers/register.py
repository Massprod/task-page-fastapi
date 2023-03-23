from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm.session import Session
from database.database import db_session
from schemas.schemas import CreateNewUser, CreateNewUserResponse


register_router = APIRouter(prefix="/register",
                            tags=["register"],
                            )


@register_router.post("/new",
                      name="Register New User",
                      response_model= CreateNewUserResponse,
                      )
async def register_new_user(request: Request,
                            user_data: CreateNewUser,
                            db: Session = Depends(db_session),
                            ):
    return ...
