from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

  class Config:
    orm_mode = True

class PostCreate(PostBase):
  pass


class PostResponse(PostBase):
  id:int
  created_at: datetime
  owner_id: int


class UserCreate(BaseModel):
  email:EmailStr
  password:str

  class Config:
    orm_mode = True

class UserResponse(BaseModel):
  id: str
  email:EmailStr

  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token:str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None


class Vote(BaseModel):
  post_id:int
  dir: int