from fastapi import APIRouter, Depends, Path
from auth.oauth2 import get_current_user
from sqlalchemy.orm.session import Session
from database.database import db_session
from schemas.user_schemas import CreateNewUser, CreateNewUserResponse, ActiveUser, UpdateUser, UpdateUserResponse
from routers.user_func.functional import create_new_user, update_user_credentials, delete_user_credentials

user_router = APIRouter(prefix="/user",
                        tags=["user"],
                        )


@user_router.post("/new",
                  name="New User",
                  response_model=CreateNewUserResponse,
                  description="Register new User with given credentials",
                  response_description="Successful response with Id and Login of registered User",
                  )
async def register_new_user(request: CreateNewUser,
                            db: Session = Depends(db_session),
                            ):
    return create_new_user(request, db)


@user_router.put("{user_id}",
                 name="Update user",
                 response_model=UpdateUserResponse,
                 response_description="Successful response with Id and New login of updated User"
                 )
async def update_exist_user(request: UpdateUser,
                            user_id: int = Path(title="User Id",
                                                description="Id of registered User"),
                            current_user: ActiveUser = Depends(get_current_user),
                            db: Session = Depends(db_session)
                            ):
    return update_user_credentials(request=request, user_id=user_id, current_user=current_user, db=db)


@user_router.delete("{user_id}",
                    name="Delete User",
                    description="Delete user and all associated Tasks data from Db with given UserId as identifier",
                    )
async def delete_exist_user(user_id: int = Path(title="User Id",
                                                description="Id of registered User",
                                                ),
                            current_user: ActiveUser = Depends(get_current_user),
                            db: Session = Depends(db_session),
                            ):
    return delete_user_credentials(user_id=user_id, current_user=current_user, db=db)
