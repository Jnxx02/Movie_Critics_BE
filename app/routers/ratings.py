from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, auth, models
from app.dependensi import get_db

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/", response_model=schemas.Rating, dependencies=[Depends(auth.get_current_active_user)])
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    return crud.create_rating(db=db, rating=rating)

@router.get("/average/{movie_id}", response_model=float, dependencies=[Depends(auth.get_current_active_user)])
def get_average_rating(movie_id: int, db: Session = Depends(get_db)):
    ratings = db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()
    if not ratings:
        raise HTTPException(status_code=404, detail="No ratings found for this movie")
    average_rating = sum(rating.rating for rating in ratings) / len(ratings)
    return average_rating

@router.get("/{movie_id}/user/{user_id}", response_model=schemas.Rating, dependencies=[Depends(auth.get_current_active_user)])
def get_rating_by_movie_and_user(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    rating = crud.get_rating_by_movie_and_user(db, movie_id=movie_id, user_id=user_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating