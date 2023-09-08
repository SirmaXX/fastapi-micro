
from fastapi import APIRouter,Depends, Request,HTTPException
from flask import jsonify
from sqlalchemy.orm import Session
import json
from app.Models.models import SessionLocal,User,Role,Permission
from app.Schemas.schema import UserCreate,RoleCreate,PermissionCreate




import hashlib
import jwt
from fastapi.encoders import jsonable_encoder

from datetime import datetime

usersroute = APIRouter(responses={404: {"description": "Not found"}})



# Dependency
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




@usersroute.get("/roles/")
async def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@usersroute.post("/roles/")
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@usersroute.get("/permissions/")
async def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return permissions

@usersroute.post("/permissions/")
async def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    db_permission =Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission



@usersroute.get("/health",description="servisin çalışıp çalışmadığını kontrol eden router")
async def health(req: Request): 
    health=True
    if health==True:
        return True
    else:
        return None





@usersroute.get("/", description="Bütün kullanıcıların sıralandığı fonksiyon")
async def home(req: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    if users != None:
        return users
    else :
        return {}
  
   


@usersroute.post("/add",description="kullanıcı ekleme fonksiyonu")
async def add_user(user:UserCreate,req: Request,db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.Pass=hashed_password
     # Create a new User instance with the provided data
    new_user = User(**user.dict())

    # Add the new user to the database session
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@usersroute.delete("/softdelete/{id}", description="kullanıcının bilgilerini silen fonksiyon")
async def change_user_status(user_id: int, new_status: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.ID == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    user.user_status = new_status
    db.commit()


    
@usersroute.delete("/delete/{id}", description="kullanıcının bilgilerini silen fonksiyon")
async def del_user(req: Request, id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(ID=id).first()
    if user is not None:
        db.delete(user)
        db.commit()
    else:
       raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")


@usersroute.put("/update/{id}", description="kullanıcının bilgilerini güncelleyen fonksiyon")
async def update_user(id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(ID=id).first()
    
    if user:
        for attr, value in user_update.dict().items():
            setattr(user, attr, value)
        
        db.commit()
        db.refresh(user)
        return user
    else:
         raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")