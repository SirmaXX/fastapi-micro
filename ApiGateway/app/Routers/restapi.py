
from fastapi import APIRouter,Depends, Request,HTTPException,Response
from flask import jsonify
from sqlalchemy.orm import Session
import urllib,json,requests
from app.Schemas.schema import User_Schema
from app.Controller.Api_User_Controller import Api_User_Controller
from pydantic import BaseModel
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse


from app.Lib.helper import log_session_activity


limiter = Limiter(key_func=get_remote_address)
restapiroute = APIRouter(responses={404: {"description": "Not found"}})



Users_Url="http://users:5002/users/"
Log_Url="http://log_service:5004/"




@restapiroute.get("/home")
@log_session_activity
@limiter.limit("5/minute")
async def homepage(request: Request, response: Response):
    return { "message": "hello world" }



@restapiroute.get("/")
@restapiroute.get("/index")
@log_session_activity
async def api_index(request: Request ,response: Response):
   return {"rest api service"}


#KULLANICILARIN REQUESTİ  BAŞLANGIÇ

@restapiroute.get("/users",description="Kullanıcıların bulunduğu liste")
async def users_panel(request: Request):
    return  Api_User_Controller.GetUsers(Users_Url)




@restapiroute.post("/adduser", description="kullanıcı ekleme fonksiyonu")
async def createuser(request: Request, user: User_Schema):
    response = Api_User_Controller.AddUser(user.Name,user.User_name,user.user_email ,user.Pass, Users_Url)
    
    if response.status_code == 200:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail="User creation failed")


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
  return  Api_User_Controller.Post_UpdateUser(id,user.Name,user.User_name,user.user_email ,user.Pass,user.user_status, Users_Url)
       



 #@restapiroute.post("/logincheck", description="kullanıcınun bilgilerini kontrol eden  fonksiyon ")
#async def logincheck(request: Request,username:str,password:str):
 #       json_user={"username": username , "password": password }
 #       checklogin=requests.post("http://job:5001/users/login", json =json_user)
 #       if (checklogin.text =="true"):
 #          return True   
 #       else:
 #         return False
       
        


#LOGLAR
@restapiroute.get("/logs",description="logların bulunduğu fonksiyon")
async def logs(request: Request):
    response = urllib.request.urlopen(Log_Url)
    data = response.read()
    dict = json.loads(data)
    return dict



#PERMİSSİONLAR
@restapiroute.get("/permission",description="logların bulunduğu fonksiyon")
async def permission(request: Request):
    response = urllib.request.urlopen(Users_Url+"permissions/")
    data = response.read()
    dict = json.loads(data)
    return dict



@restapiroute.post("/permission",description="logların bulunduğu fonksiyon")
async def permission_post(request: Request):
    my_json = { "permission_name": "string"}
    url=Users_Url+"permissions/"
    response = requests.post(url, json =my_json)
    if response.status_code == 200:
        return {"message": "Permission created successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Permission creation failed")






@restapiroute.get("/deletepermission/{id}", description="kullanıcı silme fonksiyonu")
async def deletepermission(request: Request, id: int):
    url = Users_Url + 'permissions/delete/' + str(id)
    response = requests.delete(url)
    
    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        return JSONResponse(content={"error": "DELETE request failed"}, status_code=response.status_code)



#ROLES
@restapiroute.get("/roles",description="logların bulunduğu fonksiyon")
async def roles(request: Request):
    response = urllib.request.urlopen(Users_Url+"roles/")
    data = response.read()
    dict = json.loads(data)
    return dict



@restapiroute.post("/roles",description="logların bulunduğu fonksiyon")
async def roles_post(request: Request):
    my_json = {
  "role_name": "deneme"
}
    url=Users_Url+'roles/'
    response = requests.post(url, json =my_json)
    if response.status_code == 200:
        return {"message": "Roles created successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail="User creation failed")




@restapiroute.get("/deleteroles/{id}", description="kullanıcı rolünü silme fonksiyonu")
async def deleteroles(request: Request, id: int):
    url = Users_Url + 'roles/delete/' + str(id)
    response = requests.delete(url)
    
    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        return JSONResponse(content={"error": "DELETE request failed"}, status_code=response.status_code)