
from fastapi import FastAPI
import starlette.status as status
import urllib,json,requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse,RedirectResponse

from typing import Optional,List
from app.Routers.restapi import restapiroute
from app.Lib.Api_User_Controller import Api_User_Controller
from app.Lib.common import paginate,pagecount
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="apigateway", description="apigateway")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/home")
@limiter.limit("5/minute")
async def homepage(request: Request):
    return { "message": "hello world" }



app.include_router(restapiroute, prefix="/api")


Users_Url="http://job:5001/users"

Log_Url="http://log_service:5004/"




@app.get("/")
@app.get("/index")
async def api_index(request: Request):
   return {"debug": "arayüz"}






#UYGULAMALARIN REQUESTİ  BİTİŞ
#KULLANICILARIN REQUESTİ  BAŞLANGIÇ

@app.get("/users",description="Kullanıcıların bulunduğu liste")
async def users_panel(request: Request):
    dict = Api_User_Controller.GetUsers("http://job:5001/users")
    if dict == {}:
               return templates.TemplateResponse("users.html", {"request": request,"users":dict})
    elif len(dict) >0 and len(dict)<=10:
         return templates.TemplateResponse("users.html", {"request": request,"users":dict,"page_count":1})
    else:
          per_page=3
          page_count=pagecount(dict,per_page)
          dataset=paginate(dict,per_page,0)
          return templates.TemplateResponse("paginates/users.html", {"request": request,"users":dataset,"per_page":per_page,"page_count":int(page_count)})


    


@app.get("/users/{per_page}/{pagenumber}/", response_class=HTMLResponse,description="şirketlerin bulunduğu fonksiyon")
async def usersseperated(request: Request,pagenumber:int,per_page:int):
    dict = Api_User_Controller.GetUsers(Users_Url)
    if dict == {}:
               return templates.TemplateResponse("paginates/users.html", {"request": request,"users":dict})
    else:
     page_count=pagecount(dict,per_page)
     dataset=paginate(dict,per_page,pagenumber)
     return templates.TemplateResponse("paginates/users.html", {"request": request,"users":dataset,"per_page":per_page,"page_count":int(page_count)})






@app.post("/adduser",description="kullanıcı ekleme fonksiyonu")
async def createuser(request: Request,username:str=Form(),password:str=Form()):  
     Api_User_Controller.AddUser(username,password,Users_Url)
     return RedirectResponse(
        '/users', 
        status_code=status.HTTP_302_FOUND)



@app.get("/deleteuser/{id}",description="kullanıcı silme fonksiyonu")
async def deleteuser(request: Request,id:int):
    Api_User_Controller.DeleteUser(Users_Url,id)
    RedirectResponse(url='/users')



@app.get("/updateuser/{id}",description="kullanıcı adı ")
async def updateuser(request: Request,id:int):
    dictionary=Api_User_Controller.GetUser(Users_Url,id)
    return templates.TemplateResponse("editpages/edituser.html", {"request": request,"users":dictionary})
    

    
@app.post("/updateuser/{id}",description="kullanıcı adı ")
async def updateuser(request: Request,id:int,username:str=Form(),password:str=Form()):
    response = Api_User_Controller.Post_UpdateUser(id,username,password)
    if (response.text =="true"):
          return RedirectResponse('/users',   status_code=status.HTTP_302_FOUND)      
    else:
          return RedirectResponse('/login',   status_code=status.HTTP_302_FOUND)
       



@app.get("/login", response_class=HTMLResponse ,description="login sayfası")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/logincheck", description="kullanıcınun bilgilerini kontrol eden  fonksiyon ")
async def logincheck(request: Request,username:str=Form(),password:str=Form()):
        json_user={"username": username , "password": password }
        checklogin=requests.post("http://job:5001/users/login", json =json_user)
        if (checklogin.text =="true"):
          return RedirectResponse('/index',   status_code=status.HTTP_302_FOUND)      
        else:
          return RedirectResponse('/login',   status_code=status.HTTP_302_FOUND)
       
        





@app.post('/logout', description="çıkış fonksiyonu ")
def logout():
   return RedirectResponse('/login',   status_code=status.HTTP_302_FOUND)





@app.get("/register", response_class=HTMLResponse,description="kayıt sayfası")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#KULLANICILARIN REQUESTİ BİTİŞ



#LOGLAR
@app.get("/logs", response_class=HTMLResponse,description="logların bulunduğu fonksiyon")
async def logs(request: Request):
    response = urllib.request.urlopen(Log_Url)
    data = response.read()
    dict = json.loads(data)
    per_page=3
    page_count=pagecount(dict,per_page)
    dataset=paginate(dict,per_page,0)
    return dataset





@app.get("/logs/{per_page}/{pagenumber}/", response_class=HTMLResponse,description="logların bulunduğu fonksiyon")
async def logsseperated(request: Request,pagenumber:int,per_page:int):
    response = urllib.request.urlopen(Log_Url)
    data = response.read()
    dict = json.loads(data)
    if dict == {}:
               return dict
    else:
       page_count=pagecount(dict,per_page)
       dataset=paginate(dict,per_page,pagenumber)
       return dataset