from fastapi import APIRouter, status, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from .. import schemas, models, utils, database


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(database.get_db)]):
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Annotated[Session, Depends(database.get_db)]):
    # user = db.query(models.User).filter(models.User.id == id).first()

    statement = select(models.User).where(models.User.id == id)  # | 2.0 style
    user = db.scalars(statement).first()                         # |

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found"
        )
    return user
