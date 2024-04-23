from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from typing import Annotated
from .. import schemas, models, database, oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.JokeResponse)
def create_post(
    joke: schemas.JokeCreate,
    db: Annotated[Session, Depends(database.get_db)],
    user_id: Annotated[int, Depends(oauth2.get_current_user)]
):
    print("user_id: ", user_id)
    new_post = models.Joke(**joke.model_dump())
    db.add(new_post)
    db.commit()
    return new_post


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.JokeResponse])
def get_posts(
    db: Annotated[Session, Depends(database.get_db)],
    user_id: Annotated[int, Depends(oauth2.get_current_user)]
):
    statement = select(models.Joke)
    jokes = db.scalars(statement).all()
    return jokes


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.JokeResponse)
def get_post(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    user_id: Annotated[int, Depends(oauth2.get_current_user)]
):
    statement = select(models.Joke).where(models.Joke.id == id)
    joke = db.scalars(statement).first()
    if not joke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joke with id: {id} not found"
        )
    return joke


@router.put("/{id}", response_model=schemas.JokeResponse)
def update_post(
    id: int,
    joke: schemas.JokeUpdate,
    db: Annotated[Session, Depends(database.get_db)],
    user_id: Annotated[int, Depends(oauth2.get_current_user)]
):
    to_update_joke = db.query(models.Joke).filter(models.Joke.id == id).first()
    if not to_update_joke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joke with id: {id} not found"
        )
    statement = \
        update(models.Joke) \
        .where(models.Joke.id == id) \
        .values(**joke.model_dump())
    db.execute(statement)
    db.commit()
    updated_joke = db.query(models.Joke).filter(models.Joke.id == id).first()
    return updated_joke


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    user_id: Annotated[int, Depends(oauth2.get_current_user)]
):
    to_delete_joke = db.query(models.Joke).filter(models.Joke.id == id).first()
    if not to_delete_joke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joke with id: {id} not found"
        )
    statement = \
        delete(models.Joke) \
        .where(models.Joke.id == id)
    db.execute(statement)
    db.commit()
    return to_delete_joke
