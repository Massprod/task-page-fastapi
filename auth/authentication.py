from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import db_session
from database.models import DbUsers
from auth import oauth2

auth_router = APIRouter(tags=["authentication"])


@auth_router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends(),
              db: Session = Depends(db_session),
              ):
    username = request.username.lower()
    password = request.password
    user_exist = db.query(DbUsers).filter(DbUsers.username == username).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Credentials incorrect",
                            )
    elif user_exist.password != password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Password incorrect",
                            )
    access_token = oauth2.create_access_token(data={"sub": user_exist.username})
    return {"access_token": access_token,
            "token_type": "bearer",
            "user_id": user_exist.user_id,
            "username": user_exist.username,
            }
