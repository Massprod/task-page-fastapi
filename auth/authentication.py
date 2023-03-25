from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import db_session
from database.crud.db_users import get_user
from database.hash import Hash
from auth import oauth2

auth_router = APIRouter(tags=["authentication"])


@auth_router.post("/token")
async def get_token(request: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(db_session),
                    ):
    """Create and set authentication Token"""
    login = request.username.lower()
    password = request.password
    exist = get_user(user_id=None, login=login, db=db)
    if not exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Login incorrect",
                            )
    hashed_password = exist.password
    password_correct = Hash().verify_pass(hashed_password, password)
    if not password_correct:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Password incorrect",
                            )
    access_token = oauth2.create_access_token(data={"sub": exist.login},
                                              expire_minutes=30,
                                              )
    token = {"access_token": access_token,
             "token_type": "bearer",
             "user_id": exist.user_id,
             "login": exist.login,
             }
    return token
