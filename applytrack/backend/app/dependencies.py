from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .security import decode_subject

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    subject = decode_subject(token)
    if subject is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.get(User, int(subject))
    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user
