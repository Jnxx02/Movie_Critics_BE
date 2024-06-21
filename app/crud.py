from sqlalchemy.orm import Session
from app import models, schemas, crud
from fastapi import HTTPException

# Users
def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if password != user.hashed_password:
        return False
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=user.password,
        role=user.role,
        bio=user.bio,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.role == 'critic':
        db_critic = models.Critic(
            name=user.name,
            email=user.email,
            bio=user.bio,
            author_id=db_user.id
        )
        db.add(db_critic)
        db.commit()
        db.refresh(db_critic)
        
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict().items():
        if key not in ("role", "email"):
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Movies
def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def update_movie(db: Session, movie_id: int, movie: schemas.MovieCreate):
    db_movie = get_movie(db, movie_id)
    if db_movie:
        for key, value in movie.dict().items():
            setattr(db_movie, key, value)
        db.commit()
        db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = get_movie(db, movie_id)
    if db_movie:
        db.delete(db_movie)
        db.commit()
    return db_movie

# Critics
def get_critics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Critic).offset(skip).limit(limit).all()

def get_critic(db: Session, critic_id: int):
    return db.query(models.Critic).filter(models.Critic.id == critic_id).first()

def get_critic_by_user_id(db: Session, user_id: int):
    return db.query(models.Critic).filter(models.Critic.author_id == user_id).first()

# Reviews
def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def update_review(db: Session, review_id: int, review: schemas.ReviewCreate):
    db_review = get_review(db, review_id)
    if db_review:
        for key, value in review.dict().items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review

def get_reviews_by_movie(db: Session, movie_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.movie_id == movie_id).offset(skip).limit(limit).all()

# Comments
def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, comment: schemas.CommentCreate):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment.dict().items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment

def get_comments_by_movie(db: Session, movie_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).offset(skip).limit(limit).all()

# Rating
def create_rating(db: Session, rating: schemas.RatingCreate):
    # Check if the user has already rated the movie
    existing_rating = db.query(models.Rating).filter(
        models.Rating.user_id == rating.user_id,
        models.Rating.movie_id == rating.movie_id
    ).first()
    
    if existing_rating:
        raise HTTPException(status_code=400, detail="User has already rated this movie")
    
    db_rating = models.Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating_by_movie_and_user(db: Session, movie_id: int, user_id: int):
    return db.query(models.Rating).filter(
        models.Rating.movie_id == movie_id,
        models.Rating.user_id == user_id
    ).first()
