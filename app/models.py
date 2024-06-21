from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.schemas import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    bio = Column(String(255))
    role = Column(SQLEnum(UserRole, name="userrole"), default=UserRole.USER)
    is_active = Column(Boolean, default=True)

    comments = relationship("Comment", back_populates="author")
    critic_profile = relationship("Critic", uselist=False, back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    genre = Column(String(50))
    synopsis = Column(String(255))
    duration = Column(Integer)
    release_year = Column(Integer)
    cover = Column(String(255))
    trailer = Column(String(255))

    reviews = relationship("Review", back_populates="movie")
    comments = relationship("Comment", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")

class Critic(Base):
    __tablename__ = "critics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    bio = Column(String(255))
    author_id = Column(Integer, ForeignKey('users.id'), unique=True)

    user = relationship("User", back_populates="critic_profile")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50), index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    content = Column(String(1000))

    author = relationship("User", back_populates="comments")
    movie = relationship("Movie", back_populates="comments")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float, nullable=False)

    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50), index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    content = Column(String(5000))

    movie = relationship("Movie", back_populates="reviews")
    user = relationship("User", back_populates="reviews")