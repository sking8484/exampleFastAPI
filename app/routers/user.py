
from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from fastapi.params import Body

from random import randrange
import mysql.connector as sqlconnection
from utils import dbInfo, models
from .. import schemas, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
  tags = ['Users']
)



@router.post('/users', response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(dbInfo.get_db)):
  user_dict = user.dict()
  user_dict['password'] = utils.hash(user_dict['password'])
  new_user = models.User(**user_dict)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

@router.get('/users', response_model=List[schemas.UserResponse])
def create_user(db: Session = Depends(dbInfo.get_db), current_user:int = Depends(oauth2.get_current_user)):
  users = db.query(models.User).all()
  return users


@router.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db:Session = Depends(dbInfo.get_db), current_user:int = Depends(oauth2.get_current_user)):
  user = db.query(models.User).filter(models.User.id == id).first()
  return user