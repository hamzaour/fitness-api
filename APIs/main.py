
from fastapi import FastAPI
from database import engine
from model import Base
from routers import workouts, auth

app = FastAPI()

# Create tables (if not already created)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(workouts.router)
app.include_router(auth.router)
