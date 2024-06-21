from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, auth, models
from app.dependensi import get_db

router = APIRouter(prefix="/critics", tags=["critics"])

@router.get("/", response_model=list[schemas.Critic])
def read_critics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    critics = crud.get_critics(db, skip=skip, limit=limit)
    return critics

@router.get("/{critic_id}", response_model=schemas.Critic, dependencies=[Depends(auth.get_current_active_user)])
def read_critic(critic_id: int, db: Session = Depends(get_db)):
    db_critic = crud.get_critic(db, critic_id=critic_id)
    if db_critic is None:
        raise HTTPException(status_code=404, detail="Critic not found")
    return db_critic