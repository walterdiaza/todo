from sqlalchemy import  Column, Integer, String, Sequence, Enum, ForeignKey, DATE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_name = Column(String(50))
    password = Column(String(60))
    profile_picture = Column(String(50))
    #tasks_list = Column(String(50))

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(50))
    description = Column(String(50))

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    description = Column(String(400))
    create_date = Column(DATE)
    finish_date = Column(DATE)
    status = Column(Enum('pending', 'in_progress', 'finished'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

