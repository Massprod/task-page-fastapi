from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from database.database import db_session
from database.crud.db_users import get_user

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = '3382fcde33c2b85e3ffb68acf0bdcac9499dcf427f105b1e1388a7d96a783130'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expire_minutes: int = None):
    to_encode = data.copy()
    if expire_minutes:
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_schema),
                     db: Session = Depends(db_session),
                     ):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"},
                                          )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(login=login, user_id=None, db=db)
    if user is None:
        raise credentials_exception
    return user

