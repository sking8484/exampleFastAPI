
import http
from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from random import randrange
import mysql.connector as sqlconnection
from utils import dbInfo, models
from .. import schemas, utils, oauth2


router = APIRouter(
  prefix = '/posts',
  tags=['Posts']
)



@router.get('/', response_model=List[schemas.PostResponse] )
def getPosts(current_user: int =  Depends(oauth2.get_current_user), db: Session = Depends(dbInfo.get_db), limit:int = 10):

  posts = db.query(models.Post).all()

  return list(posts)

@router.post('/', response_model=schemas.PostResponse)
def createPosts(post: schemas.PostCreate, current_user: dict =  Depends(oauth2.get_current_user), db:Session = Depends(dbInfo.get_db)):
  # title str, content str
  post = post.dict()

  post['owner_id'] = current_user.id
  newPost = models.Post(**post)

  db.add(newPost)
  db.commit()
  db.refresh(newPost)
  return newPost


@router.get('/{id}', response_model=schemas.PostResponse)
def getPost(id: int,current_user: int =  Depends(oauth2.get_current_user), db: Session = Depends(dbInfo.get_db)):
  data = db.query(models.Post).filter(models.Post.id == id).first()
  print(data)
  return data


@router.delete('/{id}')
def delete_post(id, current_user: int =  Depends(oauth2.get_current_user), db: Session = Depends(dbInfo.get_db)):
  post = db.query(models.Post).filter(models.Post.id == id)
  if not post.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

  if post.first().owner_id != current_user['id']:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

  post.delete(synchronize_session=False)
  db.commit()
  return f'Deleted Post {id}'