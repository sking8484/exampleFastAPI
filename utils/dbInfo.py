
from distutils.command.config import config
import mysql.connector as sqlconnection
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector://{settings.database_user}:{settings.database_password}@{settings.database_host}/{settings.database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class credentials:
  def __init__(self):

    self.dbCredentials = {
      "host":settings.database_host,
      "user":settings.database_user,
      "password":settings.database_password,
      "database" : settings.database
      }

class createTables:
  def __init__(self):
    credents = credentials()
    try:
      self.cnxn = sqlconnection.connect(**credents.dbCredentials)
      self.cursor = self.cnxn.cursor(dictionary = True)
      print('Datebase connected')
    except Exception as e:
      print('Connection Failed')
      print('Error: ' f"{e}")

  def CreateUserTable(self):

    self.cnxn.commit()
    tableName = 'users'
    columns = {
      'email': ['VARCHAR(255)', 'NOT NULL', 'UNIQUE'],
      'password': ['VARCHAR(255)', 'NOT NULL'],
      'id': ['BIGINT', 'NOT NULL', 'AUTO_INCREMENT'],
      'created_at':['datetime', 'NOT NULL', 'DEFAULT NOW()'],
      'PRIMARY KEY(id)':[]
    }

    sql = 'CREATE TABLE ' + tableName + '(' + ', '.join([f"{col} {' '.join(columns[col])}" for col in columns]) + ')'
    self.cursor.execute(sql)
    self.cnxn.commit()
    return 'Table Created'



def connectDB(func):

  def wrapper(*args, **kwargs):

    credents = credentials()
    try:
      cnxn = sqlconnection.connect(**credents.dbCredentials)
      cursor = cnxn.cursor(dictionary = True)
      print('Datebase connected')
    except Exception as e:
      print('Connection Failed')
      print('Error: ' f"{e}")

    returnVal =  func(cursor = cursor, cnxn = cnxn, *args, **kwargs)
    cnxn.close()

    return returnVal

  return wrapper

