from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    name: str
    username: str
    email: EmailStr
    phone_number: Optional[str] = None

class UserUpdate(BaseModel):
    model_config = {"from_attributes": True}
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None

class PasswordUpdate(BaseModel):
    model_config = {"from_attributes": True}
    old_password: str
    new_password: str

class UserLogin(BaseModel):
    model_config = {"from_attributes": True}
    username: str
    password: str