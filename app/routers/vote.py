from email.policy import HTTP
from os import access
from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas
import mysql.connector as sqlconnection
from utils import dbInfo
from .. import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(prefix = '/vote',
tags = ['Vote'])


@router.post('/', status_code = status.HTTP_201_CREATED)
def vote(currVote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user),cursor = None, cnxn = None):
  print('voting')

  @dbInfo.connectDB
  def doFunc(currVote, cursor, cnxn):

    SQL = "SELECT * FROM likes WHERE post_id = %s AND user_id = %s"
    cursor.execute(SQL, (currVote.post_id,current_user['id']))
    result = cursor.fetchone()

    if (currVote.dir == 1):
      if result:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user['id']} has already voted on {currVote.post_id}")
      new_voteSQL = "INSERT INTO likes (user_id, post_id) VALUES (%s, %s)"
      cursor.execute(new_voteSQL, (current_user['id'], currVote.post_id))
      cnxn.commit()
      return {"message":"succesfully added vote"}
    else:
      if not result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist")
      else:
        deleteSQL = "DELETE FROM likes WHERE user_id = %s and post_id = %s"

        cursor.execute(deleteSQL, (current_user['id'], currVote.post_id))
        cnxn.commit()
        return {"message":f"Deleted vote with id {currVote.post_id}"}
  return doFunc(currVote)

