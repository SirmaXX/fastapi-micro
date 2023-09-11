from fastapi import APIRouter, Request,Response
from app.models.log import Log
from app.config.db import conn 
from app.schemas.log import serializeDict, serializeList
from time import gmtime, strftime
from bson import ObjectId

log = APIRouter() 


now=strftime("%Y-%m-%d %H:%M:%S", gmtime())



#HTTP Requestler için endpointler

@log.get('/',description="logları listeleyen request")
async def distinct_log():
    return serializeList(conn.testlogdb.log.find())


@log.get('/different/', description="Farklı user agentları listeleyen request")
async def distinct_log():
    distinct_user_agents = conn.testlogdb.log.distinct('user_agent')
    return distinct_user_agents


@log.get('/differentcount/', description="Farklı user agentları sayıları ile birlikte listeleyen request")
async def distinct_log():
    pipeline = [
        {
            '$group': {
                '_id': '$user_agent',
                'count': {'$sum': 1}
            }
        },
        {
            '$project': {
                '_id': 0,
                'user_agent': '$_id',
                'count': 1
            }
        }
    ]

    result = conn.testlogdb.log.aggregate(pipeline)
    return list(result)


@log.get('/{id}',description="tekil logu listeleyen request")
async def find_one_log(id):
    return serializeDict(conn.testlogdb.log.find_one({"_id":ObjectId(id)}))


@log.post('/',description="log oluşturan post requesti")
async def create_log(log: Log):
    conn.testlogdb.log.insert_one(dict(log))
    return serializeList(conn.testlogdb.log.find())

@log.put('/{id}',description="log güncelleştiren put requesti")
async def update_log(id,log: Log):
    conn.testlogdb.log.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(log)
    })
    return serializeDict(conn.testlogdb.log.find_one({"_id":ObjectId(id)}))

@log.delete('/{id}',description="log silen delete requesti")
async def delete_log(id):
    return serializeDict(conn.testlogdb.log.find_one_and_delete({"_id":ObjectId(id)}))




#örnek log yapısı
@log.get("/items/{message}",description="örnek  log requesti")
async def read_root( request: Request,response: Response,message:str):
     log_prefix = f"('{request.headers['user-agent']}',{request.client.host}', {request.client.port}) - \"{request.method} {request.url.path} {request.headers['host']}- \"{response.status_code},{now},{message}"
     return {log_prefix}
