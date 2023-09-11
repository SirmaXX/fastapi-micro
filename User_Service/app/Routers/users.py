
from fastapi import APIRouter,Depends, Request,HTTPException
from flask import jsonify
from sqlalchemy.orm import Session
from app.Models.models import SessionLocal,User,Role,Permission
from app.Schemas.schema import UserCreate,RoleCreate,PermissionCreate,Token
from pydantic import BaseModel
import hashlib
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt



from datetime import datetime



usersroute = APIRouter(responses={404: {"description": "Not found"}})


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



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
    if roles != None:
        return roles
    else :
        raise HTTPException(status_code=404, detail="rol bulunamadı")
    


@usersroute.post("/roles/")
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role



@usersroute.delete("/roles/delete/{id}", description="kullanıcının rolünü silen fonksiyon")
async def del_roles(req: Request, id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter_by(role_id=id).first()
    if role is not None:
        db.delete(role)
        db.commit()
        return role
    else:
        raise HTTPException(status_code=404, detail="Rol bulunamadı")



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



@usersroute.delete("/permissions/delete/{id}", description="kullanıcının bilgilerini silen fonksiyon")
async def del_permission(req: Request, id: int, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter_by(permission_id=id).first()
    if permission is not None:
        db.delete(permission)
        db.commit()
    else:
       raise HTTPException(status_code=404, detail="İzin bulunamadı")
    

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
    hashed_password = hash_password(user.Pass)
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
    



@usersroute.get("/usercheckroles/{user_id}")
async def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.ID == user_id).first()

    if user is None:
        return []
    else :
        return user.role.role_name

    


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return username



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




@usersroute.post("/login", response_model=Token, description="Kullanıcının logini için oluşturulan endpoint")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.User_name == form_data.username).first()
    if db_user and verify_password(form_data.password, db_user.Pass):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@usersroute.get("/protected", description="örnek endpoint")
async def protected_endpoint(current_user: str = Depends(get_current_user)):
    # Your protected endpoint logic here
    return {"message": f"Hello, {current_user}! This is a protected endpoint."}