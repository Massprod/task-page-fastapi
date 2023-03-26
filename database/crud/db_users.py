from sqlalchemy.orm import Session
from database.models import DbUsers
from schemas.schemas import CreateNewUser
from database.hash import Hash
from typing import Type


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
    get_login = login.lower()
    if user_id:
        user = db.query(DbUsers).filter_by(id=user_id).first()
        return user
    user = db.query(DbUsers).filter_by(login=get_login).first()
    return user


def update_user(user_id: int | None, login: str | None, db: Session, request: CreateNewUser) -> Type[DbUsers] | bool:
    """Find record in DbUsers with given user_id or login. Update record with new data."""
    new_login = request.login.lower().strip()
    new_hash_password = Hash().bcrypt_pass(request.password).strip()
    if user_id:
        user = get_user(login=None, user_id=user_id, db=db)
        if user is None:
            return False  # can't use UPDATE on object given by .first()
        db.query(DbUsers).filter_by(user_id=user_id).update({
            DbUsers.login: new_login,
            DbUsers.password: new_hash_password,
        })
        db.commit()
        db.refresh(user)
        return user
    user = get_user(login=login, user_id=None, db=db)
    if user is None:
        return False
    db.query(DbUsers).filter_by(login=login).update({
        DbUsers.login: new_login,
        DbUsers.password: new_hash_password,
    })
    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id: int | None, login: str | None, db: Session) -> bool:
    """Delete record from DbUsers with given user_id or login."""
    del_login = login.lower()
    if user_id:
        user = get_user(login=None, user_id=user_id, db=db)
        if user is None:
            return False
        db.delete(user)
        db.commit()
        return True
    user = get_user(login=del_login, user_id=None, db=db)
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True
