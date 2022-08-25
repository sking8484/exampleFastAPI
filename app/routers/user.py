
from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, APIRouter
from fastapi.params import Body

from random import randrange
import mysql.connector as sqlconnection
from utils import dbInfo
from .. import schemas, utils

credents = dbInfo.credentials()
router = APIRouter(
  tags = ['Users']
)

try:
  cnxn = sqlconnection.connect(**credents.dbCredentials)
  cursor = cnxn.cursor(dictionary = True)
  print('Datebase connected')
except Exception as e:
  print('Connection Failed')
  print('Error: ' f"{e}")




@router.post('/users', response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate):
  user_dict = user.dict()
  user_dict['password'] = utils.hash(user_dict['password'])
  print(user_dict)
  cols = user_dict.keys()

  sql = 'INSERT INTO users (' + ', '.join(cols) + ')VALUES(%s, %s)'
  print([user_dict[col] for col in cols])
  cursor.execute(sql, [user_dict[col] for col in cols])
  cnxn.commit()
  user_dict['id'] = cursor.lastrowid
  return user_dict

@router.get('/users', response_model=List[schemas.UserResponse])
def create_user():
  sql = 'SELECT * FROM users'
  cursor.execute(sql)
  return cursor.fetchall()


@router.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int):
  sql = 'SELECT * FROM users WHERE id = %s'
  cursor.execute(sql, (id, ))
  user = cursor.fetchone()
  if not user:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id: {id} does not exist')
  return user