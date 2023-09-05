from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI,UploadFile,File,Request,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.Lib.helper import createLog
import urllib,json,requests


from datetime import datetime



class Api_User_Controller:

  def GetUsers(url:str):
    response = urllib.request.urlopen(url)
    data = response.read()
    dictt = json.loads(data)
    createLog("Info","kullanıcılar çağırıldı")
    return dictt


  def AddUser(username:str,password:str,url:str):
     my_json={"username":username,"password": password}    
     response= requests.post(url+"/add", json =my_json)
     return response
  
   
 
  def DeleteUser(Users_Url:str,id:int):
     url=Users_Url+'/delete/'+str(id)
     response = requests.delete(url)
     return response

 
  def GetUser(Users_Url:str,id:int):
     url=Users_Url+'/'+str(id)
     response = urllib.request.urlopen(url)
     data = response.read()
     dictionary = json.loads(data)
     return dictionary


  def Post_UpdateUser(id:int,username:str,password:str):
    json_user={"username": username , "password": password }
    url='http://job:5001/users/update/'+str(id)
    response = requests.put(url, json =json_user)
    return response



  def GetHealth():
     health=True
     if health==True:
        return True
     else:
        return None

