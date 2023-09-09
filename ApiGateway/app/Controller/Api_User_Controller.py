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
  @staticmethod
  def GetUsers(url:str):
    response = urllib.request.urlopen(url)
    data = response.read()
    dictt = json.loads(data)
    #createLog("Info","kullanıcılar çağırıldı")
    return dictt



  
  @staticmethod
  def AddUser(Name: str,User_name: str, user_email:str,Pass: str, url: str):
        my_json = {"Name": Name,"User_name": User_name,"user_email":user_email, "Pass": Pass, "user_status": True}    
        response = requests.post(url + "add", json=my_json)
        return response
  
   
 
  def DeleteUser(Users_Url:str,id:int):
     url=Users_Url+'delete/'+str(id)
     response = requests.delete(url)
     return response

 
  def GetUser(Users_Url:str,id:int):
     url=Users_Url+str(id)
     response = urllib.request.urlopen(url)
     data = response.read()
     dictionary = json.loads(data)
     return dictionary


  def Post_UpdateUser(id:int,Name: str,User_name: str, user_email:str,Pass: str,user_status:bool,Users_Url:str):
    my_json = {"Name": Name,"User_name": User_name,"user_email":user_email, "Pass": Pass, "user_status": user_status}  
    url=Users_Url+'update/'+str(id)
    response = requests.put(url, json =my_json)
    return response



  def GetHealth():
     health=True
     if health==True:
        return True
     else:
        return None

