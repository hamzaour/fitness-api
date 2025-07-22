from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from fastapi import status

from database import SessionLocal, get_db
from model import User

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic schema for user creation
class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: int = None
    gender: str = None

@router.post("/register")
def register_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    # Check if user already exists (by Email)
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        age=user.age,
        gender=user.gender
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    # 1. Check if the user exists by email
    user = db.query(User).filter(User.email == login.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falsche Anmeldedaten"
        )

    # 2. Verify password
    if not pwd_context.verify(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falsche Anmeldedaten"
        )

    return {"message": "Login erfolgreich"}