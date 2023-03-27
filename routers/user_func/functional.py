from fastapi import HTTPException, status
from database.models import DbUsers
from typing import Type
from fastapi.responses import HTMLResponse
from schemas.user_schemas import CreateNewUser, CreateNewUserResponse, UpdateUser, ActiveUser
from sqlalchemy.orm import Session
from database.crud.db_users import create_user, get_user, validate_user_id, update_user, delete_user, get_all_users


def create_new_user(request: CreateNewUser, db: Session) -> DbUsers:
    """Insert new Db record with User data"""
    request.login = request.login.lower().strip(" ").replace(" ", "")
    request.password = request.password.strip(" ").replace(" ", "")
    taken = get_user(login=request.login, user_id=None, db=db)
    if taken:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Login: {taken.login} already taken",
                            )
    new_user = create_user(db=db, request=request)
    return new_user


def update_user_credentials(request: UpdateUser,
                            user_id: int,
                            current_user: ActiveUser,
                            db: Session) -> Type[DbUsers]:
    """Update existing Db record for Active user with new User data"""
    validate_user_id(current_user=current_user, user_id=user_id)
    updated = update_user(user_id=user_id, db=db, request=request)
    if updated:
        return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"UserID: {user_id} doesn't exist",
                        )


def delete_user_credentials(user_id: int, current_user: ActiveUser, db: Session) -> HTMLResponse:
    """Delete existing Db record for Active user"""
    validate_user_id(current_user=current_user, user_id=user_id)
    deleted = delete_user(user_id=user_id, db=db)
    if deleted:
        return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"UserID: {user_id} doesn't exist",
                        )


# No reasons to use it in this practice. But if there was more data about Users to display, then it could be useful.
def get_user_data(user_id: int, current_user: ActiveUser, db: Session) -> Type[DbUsers]:
    """Getting everything about user, except password"""
    validate_user_id(user_id=user_id, current_user=current_user)
    user = get_user(user_id=user_id, login=None, db=db)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"UserID: {user_id} doesn't exist",
                        )


def get_all(current_user: ActiveUser, db: Session) -> list[Type[DbUsers]]:
    """Getting list of all users data"""
    validate_user_id(current_user=current_user, user_id=None)
    users = get_all_users(db=db)
    return users

