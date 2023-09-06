import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker,relationship # type: ignore
from sqlalchemy.sql import expression
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date
from datetime import datetime

DB_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DB_URL,
    pool_size=5,
    pool_recycle=60,
    pool_pre_ping=True)

SessionLocal = sessionmaker( bind=engine,
    autocommit=False,
    autoflush=False)

session=SessionLocal()
Base = declarative_base() 
Now = datetime.utcnow()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_reset():
   """Veritabanını sıfırlamak için hazırlan fonksiyon """
   Base.metadata.reflect(bind=engine)
   Base.metadata.drop_all(bind=engine)
   


    

class User(Base):
    """ Kullanıcı oluşturmamızı sağlayan Sınıf """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), unique=True, nullable=False)
    active = Column(Boolean, unique=False, default=True)



    def __init__(self, username,password):
     self.username =username
     self.password =password

  








Base.metadata.create_all(bind=engine)

session.commit()
