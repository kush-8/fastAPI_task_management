from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
import jwt
from src.users.models import User
from uuid import UUID
from src.utils.db import get_db


def is_authenticated(request: Request, db: Session = Depends(get_db)):
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