from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, get_db
from model import Workout
from pydantic import BaseModel
from datetime import datetime


class WorkoutCreate(BaseModel):
    name: str
    date: datetime = None
    duration_minutes: int = None
    workout_type: str = None
    owner_id : int


class WorkoutOut(BaseModel):
    id : int
    name: str
    date: datetime = None
    duration_minutes: int = None
    workout_type: str = None
    owner_id : int

    class Config:
        orm_mode = True


# --------------FastAPI Router------------------#

router = APIRouter()

# Helper function for dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET /workouts - get all workouts
@router.get("/workouts", response_model=List[WorkoutOut])
def read_workouts(db: Session = Depends(get_db)):
    workouts = db.query(Workout).all()
    return workouts

# POST /workouts - add a new workout
@router.post("/workouts", response_model=WorkoutOut)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

# Get /workouts/{workout_id} - get by id
@router.get("/workouts/{workout_id}", response_model=WorkoutOut)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

# DELETE /workouts/{workout_id} - delete a workout
@router.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
    return {"detail": "Workout deleted"}

# PUT /worktout/{workout_id} - update a workout
@router.put("/workout/{workout_id}", response_model=WorkoutOut)
def delete_update(workout_id: int, workout_update: WorkoutCreate, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    for key, value in workout_update.dict().itmes():
        setattr(workout, key, value)
    db.commit()
    db.refresh(workout_id)
    return workout