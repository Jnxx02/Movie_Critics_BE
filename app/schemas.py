from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum as PyEnum

# User
class UserRole(PyEnum):
    USER = "user"
    ADMIN = "admin"
    CRITIC = "critic"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    bio: Optional[str] = None

class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str
    role: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Movie
class MovieBase(BaseModel):
    title: str
    genre: str
    synopsis: Optional[str] = None
    duration: int
    release_year: int
    cover: str
    trailer: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        from_attributes = True

# Critic
class CriticBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str] = None
    author_id: int

class CriticCreate(CriticBase):
    pass

class Critic(CriticBase):
    id: int

    class Config:
        from_attributes = True

# Review
class ReviewBase(BaseModel):
    name: str
    content: str

class ReviewCreate(ReviewBase):
    author_id: int
    movie_id: int

class Review(ReviewBase):
    id: int
    user: User
    movie: Movie

    class Config:
        from_attributes = True

# Comment
class CommentBase(BaseModel):
    name: str
    content: str

class CommentCreate(CommentBase):
    author_id: int
    movie_id: int

class Comment(CommentBase):
    id: int
    author: User
    movie: Movie

    class Config:
        from_attributes = True

# Rating
class RatingBase(BaseModel):
    rating: float
    movie_id: int
    user_id: int

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int

    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    password: str
