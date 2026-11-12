from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .schemas import Token, UserCreate, UserRead
from .security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=email, hashed_password=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return Token(access_token=create_access_token(str(user.id)))
