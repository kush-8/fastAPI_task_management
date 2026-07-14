from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.users import controller
from src.users.dtos import UserCreate, UserLogin, UserResponse, UserUpdate
from src.utils.db import get_db

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return controller.register_user(db=db, user_data=user_data)

@user_router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def login_user(body: UserLogin, db: Session = Depends(get_db)):
    return controller.login_user(db=db, body=body)

@user_router.get("/is_authenticated", response_model=UserResponse, status_code=status.HTTP_200_OK)
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    return controller.is_authenticated(db=db, request=request)