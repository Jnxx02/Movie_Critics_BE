from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, auth, models
from app.dependensi import get_db

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/{movie_id}", response_model=list[schemas.Comment], dependencies=[Depends(auth.get_current_active_user)])
def read_comments_by_movie(movie_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments_by_movie(db, movie_id=movie_id, skip=skip, limit=limit)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this movie")
    return comments

@router.post("/", response_model=schemas.Comment, dependencies=[Depends(auth.get_role_user)])
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)

@router.put("/{comment_id}", response_model=schemas.Comment, dependencies=[Depends(auth.get_role_user)])
def update_comment(comment_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to edit this comment")
    for var, value in vars(comment).items():
        setattr(db_comment, var, value) if value else None
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}", dependencies=[Depends(auth.get_role_user)])
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if the current user is an admin
    if current_user.role == models.UserRole.ADMIN:
        db.delete(db_comment)
        db.commit()
        return {"detail": "Comment deleted"}
    elif db_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete this comment")
    
    db.delete(db_comment)
    db.commit()
    return {"detail": "Comment deleted"}
