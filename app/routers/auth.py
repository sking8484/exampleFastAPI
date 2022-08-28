from os import access
from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas
import mysql.connector as sqlconnection
from utils import dbInfo, models
from .. import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
router = APIRouter(prefix = '/login',
tags = ['authentication'])


@router.post('/', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(dbInfo.get_db)):
  user_credentials = user_credentials
  user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")


  access_token = oauth2.create_access_token(data = {'user_id':user.id})

  return {"access_token":access_token, 'token_type':'bearer'}


