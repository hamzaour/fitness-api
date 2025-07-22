from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

    # Relationship to workouts (User has many Workouts)
    workouts = relationship("Workout", back_populates='owner')


class Workout(Base):
    __tablename__= "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    data = Column(DateTime)
    duration_minutes = Column(Integer)
    workout_type = Column(String) # e.g, "Cardio", "Strenght", "Yoga"
    notes = Column(String)

    # ForeignKey to User
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="workouts")

