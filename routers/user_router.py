from fastapi import APIRouter, Depends, Path
from auth.oauth2 import get_current_user
from sqlalchemy.orm.session import Session
from database.database import db_session
from schemas.user_schemas import CreateNewUser, CreateNewUserResponse, ActiveUser, UpdateUser
from schemas.user_schemas import GetUser, UpdateUserResponse, GetAllUsers
from routers.user_func.functional import create_new_user, update_user_credentials
from routers.user_func.functional import delete_user_credentials, get_user_data, get_all
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


@user_router.get("{user_id}",
                 name="Get User",
                 response_model=GetUser,
                 description="Get data on given user_id and created Tasks by it. Only for Admin access.",
                 response_description="Successful response with id, login and all associated tasks",
                 )
async def get_user_by_id(user_id: int = Path(title="User Id",
                                             description="Id of registered User",
                                             ),
                         current_user: ActiveUser = Depends(get_current_user),
                         db: Session = Depends(db_session),
                         ):
    return get_user_data(user_id, current_user, db)


@user_router.get("/all",
                 name="Get all users",
                 response_model=GetAllUsers,
                 description="Getting list of  all existing users. Only for Admin access.",
                 response_description="Successful response with a list of all users data",
                 )
async def get_all_admin(current_user: ActiveUser = Depends(get_current_user),
                        db: Session = Depends(db_session),
                        ):
    return get_all(current_user=current_user, db=db)


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
