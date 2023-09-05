import os
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker,relationship # type: ignore
from sqlalchemy.sql import expression
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date,create_engine,DateTime,Enum
from datetime import datetime, timedelta,date

import enum

class LogInfo(enum.Enum):
    Info = "Info"
    WarningInfo= "Warning"
    Error = "Error"
    Success ="Success"



class  Log(BaseModel):
    logtype :LogInfo
    user_agent:str
    host :str
    port :str
    method :str
    path :str
    message :str
    create_time :datetime
   
    class Config:  
        use_enum_values = True
        arbitrary_types_allowed = True





class  AppLog(BaseModel):
    logtype :LogInfo
    method :str
    message :str
    create_time :datetime
   
    class Config:  
        use_enum_values = True
        arbitrary_types_allowed = True
