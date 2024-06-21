from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, auth, models
from app.dependensi import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/{movie_id}", response_model=list[schemas.Review], dependencies=[Depends(auth.get_current_active_user)])
def read_reviews_by_movie(movie_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews_by_movie(db, movie_id=movie_id, skip=skip, limit=limit)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this movie")
    return reviews

@router.post("/", response_model=schemas.Review, dependencies=[Depends(auth.get_current_active_user)])
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)

@router.put("/{review_id}", response_model=schemas.Review, dependencies=[Depends(auth.get_current_active_user)])
def update_review(review_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db_critic = db.query(models.Critic).filter(models.Critic.author_id == db_review.author_id).first()
    if db_critic is None or db_critic.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to edit this review")
    
    for var, value in vars(review).items():
        setattr(db_review, var, value) if value else None
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.delete("/{review_id}", dependencies=[Depends(auth.get_current_critic_user)])
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db_critic = crud.get_critic_by_user_id(db, user_id=current_user.id)
    # Check if the current user is an admin
    if current_user.role == models.UserRole.ADMIN:
        db.delete(db_review)
        db.commit()
        return {"detail": "Comment deleted"}
    elif db_review.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete this comment")
    
    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted"}


