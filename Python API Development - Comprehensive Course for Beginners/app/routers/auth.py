from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from .. import database, models, schemas, oauth2, utils


router = APIRouter(
    tags=["Authentication"]
)


def authenticate_user(
    username: str,
    password: str,
    db: Annotated[Session, Depends(database.get_db)]
):
    statement = select(models.User).where(
        models.User.email == username)
    user = db.scalars(statement).first()
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(database.get_db)]
) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
