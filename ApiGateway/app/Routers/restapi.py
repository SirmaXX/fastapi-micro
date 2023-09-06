
from fastapi import APIRouter,Depends, Request,HTTPException
from flask import jsonify
from sqlalchemy.orm import Session
import urllib,json,requests
from app.Lib.schema import User_Schema
from app.Lib.Api_User_Controller import Api_User_Controller

restapiroute = APIRouter(responses={404: {"description": "Not found"}})






Users_Url="http://job:5001/users"

Log_Url="http://log_service:5004/"




@restapiroute.get("/")
@restapiroute.get("/index")
async def api_index(request: Request):
   return {"rest api service"}


#KULLANICILARIN REQUESTİ  BAŞLANGIÇ

@restapiroute.get("/users",description="Kullanıcıların bulunduğu liste")
async def users_panel(request: Request):
    Api_User_Controller.GetUsers(Users_Url)


@restapiroute.post("/adduser",description="kullanıcı ekleme fonksiyonu")
async def createuser(request: Request,user:User_Schema):  
     Api_User_Controller.AddUser(user.username,user.password,Users_Url)


@restapiroute.get("/deleteuser/{id}",description="kullanıcı silme fonksiyonu")
async def deleteuser(request: Request,id:int):
    Api_User_Controller.DeleteUser(Users_Url,id)


@restapiroute.get("/updateuser/{id}",description="kullanıcı adı ")
async def updateuser(request: Request,id:int):
    url=Users_Url+'/' +str(id)
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return dict
    

    
@restapiroute.post("/updateuser/{id}",description="kullanıcı adı ")
async def updateuser(request: Request,id:int,user:User_Schema):
    Api_User_Controller.Post_UpdateUser(id,user.username,user.password)
       






@restapiroute.post("/logincheck", description="kullanıcınun bilgilerini kontrol eden  fonksiyon ")
async def logincheck(request: Request,username:str,password:str):
        json_user={"username": username , "password": password }
        checklogin=requests.post("http://job:5001/users/login", json =json_user)
        if (checklogin.text =="true"):
           return True   
        else:
          return False
       
        




#LOGLAR
@restapiroute.get("/logs",description="logların bulunduğu fonksiyon")
async def logs(request: Request):
    response = urllib.request.urlopen(Log_Url)
    data = response.read()
    dict = json.loads(data)
    return dict
