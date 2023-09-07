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

@applog.get('/webapplog/',description="webapplog'u listeleyen request")
async def distinct_log():
    return serializeList(conn.testlogdb.webapplog.find())



@applog.get('/webapplog/{id}',description="tekil webapplog'u listeleyen request")
async def find_one_log(id):
    return serializeDict(conn.testlogdb.webapplog.find_one({"_id":ObjectId(id)}))


@applog.post('/webapplog/',description="webapplog oluşturan post requesti")
async def create_log(log:AppLog):
    conn.testlogdb.log.insert_one(dict(log))
    return serializeList(conn.testlogdb.webapplog.find())

@applog.put('/webapplog/{id}',description="webapplog güncelleştiren put requesti")
async def update_log(id,log:AppLog):
    conn.testlogdb.log.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(log)
    })
    return serializeDict(conn.testlogdb.webapplog.find_one({"_id":ObjectId(id)}))

@applog.delete('/webapplog/{id}',description="webapplog silen delete requesti")
async def delete_log(id):
    return serializeDict(conn.testlogdb.webapplog.find_one_and_delete({"_id":ObjectId(id)}))




