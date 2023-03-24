from fastapi import HTTPException, status
from schemas.schemas import CreateNewUser, CreateNewUserResponse
from sqlalchemy.orm import Session
from database.crud.db_users import create_user, get_user


def create_new_user(user_data: CreateNewUser, db: Session) -> CreateNewUserResponse:
    """Insert new Db record with User data"""
    new_login = user_data.login
    taken = get_user(login=new_login, user_id=None, db=db)
    if taken:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Login: {taken.login} already taken")
    new_user = create_user(db=db, request=user_data)
    return new_user
