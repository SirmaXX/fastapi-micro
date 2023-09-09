
from fastapi import APIRouter,Depends, Request,HTTPException,Response
from flask import jsonify
from sqlalchemy.orm import Session
import urllib,json,requests
from app.Schemas.schema import User_Schema
from app.Controller.Api_User_Controller import Api_User_Controller

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


from functools import wraps
import logging
from time import gmtime, strftime

limiter = Limiter(key_func=get_remote_address)

restapiroute = APIRouter(responses={404: {"description": "Not found"}})






Users_Url="http://job:5001/users"

Log_Url="http://log_service:5004/"

now=strftime("%Y-%m-%d %H:%M:%S", gmtime())


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@restapiroute.get("/items/{message}",description="örnek  log requesti")
async def read_root( request: Request,response: Response,message:str):
     log_prefix = f"('{request.headers['user-agent']}',{request.client.host}', {request.client.port}) - \"{request.method} {request.url.path} {request.headers['host']}- \"{response.status_code},{now},{message}"
     return {log_prefix}




def log_session_activity(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Log the session start and end, if needed
        logger.info(f"Session started: {request.client.host}")
        url = 'http://log_service:5004/'
        
        data = {
            "logtype": "Info",
            "user_agent":str( request.headers['user-agent']),
            "host": str(request.client.host),
            "port":  str(request.client.port),
            "method": str(request.method),
            "path": str(request.url.path),
            "message": "string",
            "create_time": str(now)
        }
        
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        # Print the data being sent
        print("Sending data:", data)

        response = requests.post(url, json=data, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            response_content = response.text
            print("Response content:", response_content)
            responsee = await func(request, *args, **kwargs)
            logger.info(f"Session ended: {request.client.host} {request.method} {request.url.path} {request.headers['host']}")
            return responsee
        else:
            print('Request failed with status code:', response.status_code)
            log_prefix = f"{request.client.host} - \"{request.method} {request.url.path} {request.headers['host']}\""
            print(log_prefix)

    return wrapper




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
