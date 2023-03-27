from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse
from schemas.user_schemas import CreateNewUser, CreateNewUserResponse, UpdateUser, ActiveUser
from sqlalchemy.orm import Session
from database.crud.db_users import create_user, get_user, validate_user_id, update_user


def create_new_user(request: CreateNewUser, db: Session) -> CreateNewUserResponse:
    """Insert new Db record with User data"""
    request.login = request.login.lower().strip(" ").replace(" ", "")
    request.password = request.password.strip(" ").replace(" ", "")
    taken = get_user(login=request.login, user_id=None, db=db)
    if taken:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Login: {taken.login} already taken")
    new_user = create_user(db=db, request=request)
    return new_user


def update_user_credentials(request: UpdateUser,
                            user_id: int,
                            current_user: ActiveUser,
                            db: Session) -> HTMLResponse:
    validate_user_id(current_user=current_user, user_id=user_id)
    update_user(user_id=user_id, db=db, request=request)
    return HTMLResponse(status_code=status.HTTP_200_OK)
