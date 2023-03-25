from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
import datetime as dt
from sqlalchemy.orm.session import Session
from auth.oauth2 import create_access_token
from database.crud.db_users import get_user
from database.database import db_session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from database.hash import Hash

login_router = APIRouter(prefix="/login",
                         tags=["login"],
                         )
templates = Jinja2Templates(directory="routers/templates/login")


@login_router.get("/")
async def login_user(request: Request):
    return templates.TemplateResponse("login.html",
                                      context={"request": request,
                                               "copyright": dt.datetime.utcnow().strftime("%Y"),
                                               },
                                      )


@login_router.post("/")
async def authenticate_user(request: Request,
                            auth_data: OAuth2PasswordRequestForm = Depends(),
                            db: Session = Depends(db_session),
                            ):
    """Create and set authentication Token"""
    login = auth_data.username.lower()
    password = auth_data.password
    exist = get_user(user_id=None, login=login, db=db)
    if not exist:
        return templates.TemplateResponse("login.html",
                                          context={"request": request,
                                                   "name_inc": True,
                                                   "copyright": dt.datetime.utcnow().strftime("%Y"),
                                                   }
                                          )
    hashed_password = exist.password
    password_correct = Hash().verify_pass(hashed_password, password)
    if not password_correct:
        return templates.TemplateResponse("login.html",
                                          context={"request": request,
                                                   "pass_inc": True,
                                                   "copyright": dt.datetime.utcnow().strftime("%Y"),
                                                   }
                                          )
    access_token = create_access_token(data={"sub": exist.login},
                                       expire_minutes=30,
                                       )
    token = {"access_token": access_token,
             "token_type": "bearer",
             "user_id": exist.user_id,
             "login": exist.login,
             }
    return token
