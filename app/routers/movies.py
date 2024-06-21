from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, auth
from app.dependensi import get_db
from typing import List

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=schemas.Movie, dependencies=[Depends(auth.get_current_admin_user)])
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db=db, movie=movie)

@router.get("/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

@router.get("/{movie_id}", response_model=schemas.Movie, dependencies=[Depends(auth.get_current_active_user)])
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return db_movie

@router.put("/{movie_id}", response_model=schemas.Movie, dependencies=[Depends(auth.get_current_admin_user)])
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return crud.update_movie(db=db, movie=movie, movie_id=movie_id)

@router.delete("/{movie_id}", response_model=schemas.Movie, dependencies=[Depends(auth.get_current_admin_user)])
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return crud.delete_movie(db=db, movie_id=movie_id)
