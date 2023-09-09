
from fastapi import APIRouter,Depends, Request,HTTPException,Response
import requests
import json

from functools import wraps
import logging
from time import gmtime, strftime

now=strftime("%Y-%m-%d %H:%M:%S", gmtime())



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



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
            responsee = await func(request, *args, **kwargs)
            logger.info(f"Session ended: {request.client.host} {request.method} {request.url.path} {request.headers['host']}")
            return responsee
        else:
            print('Request failed with status code:', response.status_code)
            log_prefix = f"{request.client.host} - \"{request.method} {request.url.path} {request.headers['host']}\""
            print(log_prefix)

    return wrapper



def createLog(logtype:str,message:str):
  my_json={"logtype": logtype,"message": message}
  response =requests.post("http://log_service:5004/add", json =my_json)
  return response





