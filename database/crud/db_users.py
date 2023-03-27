from sqlalchemy.orm import Session
from database.models import DbUsers
from schemas.user_schemas import CreateNewUser, ActiveUser, UpdateUser
from database.hash import Hash
from typing import Type
from fastapi import HTTPException, status


def validate_user_id(current_user: ActiveUser, user_id: int):
    """Validate that used given user_id for update/delete is currently Active user"""
    current_user_id = current_user.id
    validate_id = user_id
    if current_user_id == validate_id:
        return True
    elif current_user_id == 1:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="You don't have access to change other Users credentials. "
                               "Make sure to use registered ID of you own.",
                        )


def create_user(db: Session, request: CreateNewUser) -> DbUsers:
    """Create a new user record in DbUsers with given data."""
    login = request.login
    hash_password = Hash().bcrypt_pass(request.password)
    user = DbUsers(login=login,
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


def get_user(user_id: int | None, login: str | None, db: Session) -> Type[DbUsers] | None:
    """Find record in DbUsers with given login or user_id. Returns found record."""
    if login:
        get_login = login.lower()
        user = db.query(DbUsers).filter_by(login=get_login).first()
        return user
    user = db.query(DbUsers).filter_by(id=user_id).first()
    return user


def update_user(user_id: int | None, db: Session, request: UpdateUser) -> Type[DbUsers] | bool:
    """Find record in DbUsers with given user_id and Update record with new data."""
    if user_id == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin can't be modified after creation",
                            )
    new_login = request.new_login.lower().strip().replace(" ", "")
    new_hash_password = Hash().bcrypt_pass(request.new_password.strip().replace(" ", ""))
    user = get_user(login=None, user_id=user_id, db=db)
    if user is None:
        return False  # can't use UPDATE on object given by .first()
    db.query(DbUsers).filter_by(id=user_id).update({
        DbUsers.login: new_login,
        DbUsers.password: new_hash_password,
    })
    db.commit()
    return user


def delete_user(user_id: int | None, db: Session) -> bool:
    """Delete record from DbUsers with given user_id."""
    if user_id == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin Id can't be deleted",
                            )
    user = get_user(login=None, user_id=user_id, db=db)
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True
