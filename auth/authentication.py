from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import db_session
from database.crud.db_users import get_user
from database.hash import Hash
from auth import oauth2
from schemas.user_schemas import AccessToken

auth_router = APIRouter(tags=["authentication"])


@auth_router.post("/token",
                  name="Oauth2 Token",
                  response_model=AccessToken,
                  description="Creating access token with set expiration time for correct Username/Password",
                  response_description="Successful response with token, token_type and user identifiers"
                  )
async def get_token(request: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(db_session),
                    ):
    """
    Create and set authentication Token for correct Username/Password.
    Raise exception '403-forbidden' otherwise.
    """
    login = request.username.lower().strip().replace(" ", "")
    password = request.password.strip().replace(" ", "")
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
    user_id = exist.id
    user_login = exist.login
    access_token = oauth2.create_access_token(data={"sub": user_login},
                                              expire_minutes=360,
                                              )
    return AccessToken(access_token=access_token,
                       user_id=user_id,
                       login=user_login,
                       )
