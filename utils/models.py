from .dbInfo import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key = True, nullable = False)
  title = Column(String(255), nullable=False)
  content = Column(String(255), nullable = False)
  published = Column(Boolean, server_default = '0')
  created_at = Column(TIMESTAMP(timezone = True), server_default = text('now()'))

  owner_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), nullable=False)



class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key = True, nullable = False)
  email = Column(String(255), nullable = False, unique=True)
  password = Column(String(255), nullable=False)
  created_at = Column(TIMESTAMP(timezone = True), server_default = text('now()'))


class Vote(Base):
  __tablename__ = 'votes'

  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
  post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)