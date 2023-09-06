from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI,UploadFile,File,Request
from fastapi.middleware.cors import CORSMiddleware

from app.Routers.users import usersroute

import os
import json


app = FastAPI(title="kullanıcı servisi", description="Kullanıcıların bulunduğu servis")
app.include_router(usersroute, prefix="/users")




@app.get("/health",description="servisin çalışıp çalışmadığını kontrol eden router")
async def health(req: Request): 
    health=True
    if health==True:
        return True
    else:
        return None



@app.get("/",description="index için router")
async def api_index():
    """ 
    iş servisinin giriş sayfası
    """
    return {"Hello": "Job"}







  