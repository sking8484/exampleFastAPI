from os import access
from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas
import mysql.connector as sqlconnection
from utils import dbInfo
from .. import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(prefix = '/login',
tags = ['authentication'])

credents = dbInfo.credentials()

try:
  cnxn = sqlconnection.connect(**credents.dbCredentials)
  cursor = cnxn.cursor(dictionary = True)
  print('Datebase connected')
except Exception as e:
  print('Connection Failed')
  print('Error: ' f"{e}")

@router.post('/', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
  user_credentials = user_credentials
  sql = "SELECT * FROM users WHERE email = %s"
  cursor.execute(sql, (user_credentials.username,))
  user = cursor.fetchone()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
  if not utils.verify(user_credentials.password, user['password']):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")


  access_token = oauth2.create_access_token(data = {'user_id':user['id']})

  return {"access_token":access_token, 'token_type':'bearer'}


