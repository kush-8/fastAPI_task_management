from src.users.dtos import UserCreate, UserLogin, UserResponse, UserUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from src.users.models import User
from uuid import UUID
from pwdlib import PasswordHash
from src.utils.settings import settings
import jwt
from datetime import datetime, timedelta, timezone
hasher = PasswordHash.recommended()

def register_user(db: Session, user_data: UserCreate):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is taken.")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered.")
        
    hashed_pwd = hasher.hash(settings.PASSWORD_SECRET + user_data.password)
    user_dict = user_data.model_dump()
    user_dict.pop("password")
    new_user = User(**user_dict, hash_password=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, body: UserLogin):
    user = db.query(User).filter(User.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    if not hasher.verify(settings.PASSWORD_SECRET + body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION_TIME)
    payload = {"user_id": str(user.id), "username": user.username, "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return {"token": token}

def is_authenticated(db: Session, request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing.")
    
    token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
        
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")