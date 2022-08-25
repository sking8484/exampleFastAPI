
from email.policy import HTTP
from sqlite3 import Cursor
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import mysql.connector as sqlconnection
from utils import dbInfo
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

credents = dbInfo.credentials()

try:
  cnxn = sqlconnection.connect(**credents.dbCredentials)
  cursor = cnxn.cursor(dictionary = True)
  print('Datebase connected')
except Exception as e:
  print('Connection Failed')
  print('Error: ' f"{e}")


def create_access_token(data:dict):
  to_encode = data.copy()

  expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

def verify_access_token(token: str, credentials_exception):

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    id: str = payload.get('user_id')
    if id is None:
      raise credentials_exception

    token_data = schemas.TokenData(id = id)
  except JWTError:
    raise credentials_exception

  return token_data

def get_current_user(token: str = Depends(oath2_scheme)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate":"Bearer"})

  token = verify_access_token(token, credentials_exception)
  SQL = 'SELECT * FROM users WHERE id = %s'

  cursor.execute(SQL, (token.id, ))
  user = cursor.fetchone()

  return user