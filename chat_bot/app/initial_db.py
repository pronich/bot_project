from settings import ENGINE
from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=False)
    tg_login = Column(String(50), unique=True)
    name = Column(String(50))
    surname = Column(String(100))
    email = Column(String(100))
    phone = Column(String(10))
    status = Column(String(20))


Base.metadata.create_all(ENGINE)
