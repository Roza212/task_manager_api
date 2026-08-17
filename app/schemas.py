from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import date

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

# Task Schemas
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    due_date: Optional[date] = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
