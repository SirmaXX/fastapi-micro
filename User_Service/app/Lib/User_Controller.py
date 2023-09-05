from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI,UploadFile,File,Request,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.Lib.models import SessionLocal,User
from app.Lib.schema import User_Schema


from datetime import datetime

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


class UserController:
  now = datetime.now()
 # Dependency

  def addUser(db: Session,user):
     new_user = User(username=user.username,password=user.password)
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user

  def deleteUser(db: Session,id:int):
    user = db.query(User).filter_by(id=id).first()
    if  user != None:
      db.delete( user)
      db.commit()
      db.refresh( user )
      return {}
    else :
        return {}


  def updateUser(db: Session,user1,id:int):
      user = db.query(User).filter_by(id=id).first()
      if user != None:
         db.query(User).filter_by(id=id).update(
         dict(username=user1.username, password=user1.password))
         db.commit()
         db.refresh(user)
         return user
      else :
         return None


  def GetUser(db: Session,id:int):
    user = db.query(User).filter_by(id=id).first()
    if user != None:
        return user
    else :
        return {}


  def Userlist(db: Session):
      return  db.query(User).all()
  
   
  def GetHealth():
     health=True
     if health==True:
        return True
     else:
        return None
