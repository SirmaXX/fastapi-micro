from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI,UploadFile,File,Request
from fastapi.middleware.cors import CORSMiddleware

from app.Routers.users import usersroute

import os
import json

def create_app():
  app = FastAPI(title="kullanıcı servisi", description="Kullanıcıların bulunduğu servis")
  app.include_router(usersroute, prefix="/users")
  return app






  