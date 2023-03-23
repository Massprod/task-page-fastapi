from fastapi import HTTPException, status
from schemas.schemas import CreateNewUser, CreateNewUserResponse
from database.models import DbUsers
from sqlalchemy.orm import Session


def create_new_user(user_data: CreateNewUser, db: Session) -> CreateNewUserResponse:
    """Insert new Db record with User data"""
    if (username := user_data.username.lower()) and (password := user_data.password):
        taken = db.query(DbUsers).filter_by(username=username).first()
        if taken:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Username for {username} already taken")
        new_user = DbUsers(username=username,
                           password=password,
                           )
        db.add(new_user)
        db.commit()
        return new_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Fill required fields: username, password")
