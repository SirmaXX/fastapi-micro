import requests
import json



def createLog(logtype:str,message:str):
  my_json={"logtype": logtype,"message": message}
  response =requests.post("http://log_service:5004/add", json =my_json)
  return response