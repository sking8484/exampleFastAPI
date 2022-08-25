
import http
from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from fastapi.params import Body

from random import randrange
import mysql.connector as sqlconnection
from utils import dbInfo
from .. import schemas, utils, oauth2


router = APIRouter(
  prefix = '/posts',
  tags=['Posts']
)


credents = dbInfo.credentials()

try:
  cnxn = sqlconnection.connect(**credents.dbCredentials)
  cursor = cnxn.cursor(dictionary = True)
  print('Datebase connected')
except Exception as e:
  print('Connection Failed')
  print('Error: ' f"{e}")



@router.get('/', response_model=List[schemas.PostResponse])
def getPosts(current_user: int =  Depends(oauth2.get_current_user), limit:int = 10):
  print(limit)
  query = "SELECT * FROM posts"
  cursor.execute(query)
  data = cursor.fetchall()
  return data

@router.post('/')
def createPosts(post: schemas.PostCreate, current_user: int =  Depends(oauth2.get_current_user)):
  # title str, content str
  print(current_user)
  post = post.dict()
  post['posts_users_fk'] = current_user['id']
  headers = ('title', 'content', 'published', 'posts_users_fk')
  query = ("INSERT INTO posts (" + ','.join(headers) + ") values (%s, %s, %s, %s)")
  vals = [post[header] for header in headers]
  cursor.execute(query, (vals))
  cnxn.commit()
  data = cursor.lastrowid
  return data



@router.get('/{id}', response_model=schemas.PostResponse)
def getPost(id: int,current_user: int =  Depends(oauth2.get_current_user)):
  query = 'SELECT * FROM posts WHERE id = (%s)'
  cursor.execute(query, (id,))
  data = cursor.fetchone()
  return data


@router.delete('/{id}')
def delete_post(id, current_user: int =  Depends(oauth2.get_current_user)):
  sql = "SELECT * FROM posts WHERE id = %s"
  cursor.execute(sql, (id, ))
  post = cursor.fetchone()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
  if post['posts_users_fk'] != current_user['id']:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

  sql = 'DELETE FROM posts WHERE id = %s AND posts_users_fk = %s'
  cursor.execute(sql, (id,current_user['id']))
  cnxn.commit()
  return f'Deleted Post {id}'