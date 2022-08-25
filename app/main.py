
from typing import Optional, List
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from random import randrange
import mysql.connector as sqlconnection
from utils import dbInfo
from . import schemas, utils
from .routers import posts, user, auth, vote
from .config import settings

credents = dbInfo.credentials()


try:
  cnxn = sqlconnection.connect(**credents.dbCredentials)
  cursor = cnxn.cursor(dictionary = True)
  print('Datebase connected')
except Exception as e:
  print('Connection Failed')
  print('Error: ' f"{e}")



app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
  return {"message":"Hello bum"}

@app.post('/createTable')
def createTable():
  tableGenerator = dbInfo.createTables()
  tableGenerator.CreateUserTable()




