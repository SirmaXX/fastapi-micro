from fastapi import APIRouter, Request,Response
from app.models.log import AppLog
from app.config.db import conn 
from app.schemas.log import serializeDict, serializeList
from time import gmtime, strftime
from bson import ObjectId
applog = APIRouter() 

#webapplog
now=strftime("%Y-%m-%d %H:%M:%S", gmtime())



#HTTP Requestler için endpointler



@applog.post('/webapplog/',description="web servislerine özel log oluşturan post requesti")
async def create_log(log:AppLog):
    conn.testlogdb.log.insert_one(dict(log))
    return serializeList(conn.testlogdb.webapplog.find())
