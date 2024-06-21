from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import crud, schemas, auth, models
from app.dependensi import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/user-profile")
async def user_profile(current_user: schemas.User = Depends(auth.get_current_active_user)):
    print (current_user)
    return {"user_id": current_user.id, "name": current_user.name, "email": current_user.email, "role" : current_user.role, "bio" : current_user.bio}

@router.put("/{user_id}", response_model=schemas.User, dependencies=[Depends(auth.get_current_active_user)])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to edit this user")
    
    # Update user data
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    
    # Check if the current user is a critic and update critic table if necessary
    if current_user.role == "critic":
        db_critic = crud.get_critic_by_user_id(db, user_id=current_user.id)
        if db_critic:
            for var, value in vars(user).items():
                if hasattr(db_critic, var):
                    setattr(db_critic, var, value) if value else None
            db.add(db_critic)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if current_user.role == "critic" and db_critic:
        db.refresh(db_critic)
    
    return db_user

@router.delete("/{user_id}", dependencies=[Depends(auth.get_current_admin_user)])
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}