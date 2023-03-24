from sqlalchemy.orm import Session
from database.models import DbUsers
from schemas.schemas import CreateNewUser
from database.hash import Hash
from fastapi import HTTPException, status
from typing import Type


def create_user(db: Session, request: CreateNewUser) -> DbUsers:
    """Create a new record in DbUsers with given data."""
    username = request.username
    hash_password = Hash().bcrypt_pass(request.password)
    user = DbUsers(username=username,
                   password=hash_password,
                   )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session) -> list[Type[DbUsers]]:
    """Find all records in DbUsers and return them."""
    all_users = db.query(DbUsers).all()
    return all_users


def get_user(username: str, db: Session, user_id: int = None) -> Type[DbUsers] | None:
    """Find record in DbUsers with given username or user_id. Returns found record."""
    if user_id:
        user = db.query(DbUsers).filter_by(user_id=user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"There's no User with id: {user_id}",
                                )
        return user
    user = db.query(DbUsers).filter_by(username=username).first()
    if username is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There's no User with username: {username}",
                            )
    return user


def update_user(username: str, db: Session, request: CreateNewUser, user_id: int = None) -> bool:
    """Find record in DbUsers with given user_id or username. Update record with new data."""
    new_username = request.username
    new_hash_password = Hash().bcrypt_pass(request.password)
    if user_id:
        user = db.query(DbUsers).filter_by(user_id=user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"There's no User with id: {user_id}",
                                )
        user.update(
            {DbUsers.username: new_username,
             DbUsers.password: new_hash_password,
             }
        )
        db.commit()
        return True
    user = db.query(DbUsers).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There's no User with username: {username}",
                            )
    user.update(
        {DbUsers.username: new_username,
         DbUsers.password: new_hash_password,
         }
    )
    db.commit()
    return True
