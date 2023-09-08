from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI,UploadFile,File,Request,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from User_Service.app.Models.models import SessionLocal,User
from User_Service.app.Schemas.schema import User,UserCreate
import hashlib
import jwt
from fastapi.encoders import jsonable_encoder

from datetime import datetime


SECRET_KEY = "secrettoken"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800



def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


#USERS
def hash_password(password):
    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def verify_password(input_password, hashed_password):
    # Hash the input password and compare it with the stored hashed password
    return hashlib.sha256(input_password.encode()).hexdigest() == hashed_password


class UserController:
  def checkuser(db: Session, user: User):
        db_user = db.query(User).filter(User.username == user.username).first()
        data = jsonable_encoder(user)
        if db_user:
            result = verify_password(user.password, db_user.password)
            if result:
                encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                return {"user_id": db_user.id,"token":encoded_jwt,"message":True}
            else:
                return False
        else:
            return False

        
            return False

  def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(User_name=user.username, Pass=hashed_password,user_email=user.email, user_status=1,insert_date=datetime.utcnow(),update_date=datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





  def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.ID== user_id).first()

  def get_user_by_username(db: Session, username:str):
    return db.query(User).filter(User.User_name == username.first())


  def get_user(db: Session, user_id: int):
     return db.query(User).filter(User.ID == user_id).first()

  def get_users(db: Session, skip: int = 0, limit: int = 10):
      return db.query(User).offset(skip).limit(limit).all()

  def update_user(db: Session, user_id: int, user: User):
    db_user = db.query(User).filter(User.ID == user_id).first()
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value is not None else None
    db.commit()
    db.refresh(db_user)
    return db_user

  def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.ID == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    else:
        return None