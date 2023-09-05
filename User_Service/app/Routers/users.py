
from fastapi import APIRouter,Depends, Request,HTTPException
from flask import jsonify
from sqlalchemy.orm import Session
import json
from app.Lib.models import SessionLocal,User
from app.Lib.schema import User_Schema,U_User_Schema


usersroute = APIRouter(responses={404: {"description": "Not found"}})



# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



@usersroute.get("/",description=" bütün kullanıcıların sıralandığı fonksiyon")
async def home(req: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        return {}
    else :
        return users
   


@usersroute.get("/{id}",description=" istenilen kullanıcının bilgilerini veren fonksiyon")
async def get_user(req: Request,id:int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=id).first()
    if user != None:
        return user
    else :
        return {}
    



@usersroute.post("/add",description="kullanıcı ekleme fonksiyonu")
async def add_user(user:User_Schema,req: Request,db: Session = Depends(get_db)):
     new_user = User(username=user.username,password=user.password)
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user
     



@usersroute.put("/update/{id}",description=" kullanıcının bilgilerini editleyen  fonksiyon ")
async def update_user(user1:U_User_Schema,id:int,db: Session = Depends(get_db)):
  user = db.query(User).filter_by(id=id).first()
  if user != None:
      db.query(User).filter_by(id=id).update(
      dict(username=user1.username, password=user1.password))
      db.commit()
      return True
  else :
     return False
 

#@usersroute.put("/update/{id}",description=" kullanıcının bilgilerini editleyen  fonksiyon ")
#async def update_user(user1:U_User_Schema,id:int,db: Session = Depends(get_db)):
#   user = db.query(User).filter_by(id=id).first()
#   if user != None:
#     db.query(User).filter_by(id=id).update(
 #    dict(username=user1.username, password=user1.password))
#     db.commit()
 #    return "Kullanıcı bilgileri güncellendi"
 #  else :
#     return "Kullanıcı bilgileri güncellenmedi"
 



@usersroute.delete("/delete/{id}" ,description=" kullanıcınun bilgilerini silen  fonksiyon ")
async def del_user(req: Request,id:int,db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=id).first()
    if user != None:
      db.delete(user)
      db.commit()
      db.refresh(user )
    else :
      return {}
     
   


@usersroute.post("/login",description="kullanıcınun bilgilerini kontrol eden  fonksiyon ")
async def check_user(req: Request,user1:User_Schema,db: Session = Depends(get_db)):
     user = db.query(User).filter(User.username ==  user1.username, User.password== user1.password).first()
     if user != None:
        return True
     else :
        return False                                   

  


