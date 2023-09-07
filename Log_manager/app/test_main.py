from fastapi.testclient import TestClient 

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Job"}



def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == True
    
dataset  = [{"active":True,"message":"stringdeneme","create_time":"2023-01-17T23:13:34.638873","id":1,"logtype":"Info"},{"active":True,"message":"kullanıcılar çağırıldı","create_time":"2023-01-21T16:19:02.311792","id":2,"logtype":"Info"},{"active":True,"message":"kullanıcılar çağırıldı","create_time":"2023-01-21T16:19:07.050022","id":3,"logtype":"Info"},{"active":True,"message":"kullanıcılar çağırıldı","create_time":"2023-01-21T16:20:19.383410","id":4,"logtype":"Info"}]


def test_logs():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == dataset

postlog={
  "logtype": "Info",
  "message": "string"
}

def test_post_log():
    response = client.post("/add", json=postlog)
    assert response.status_code == 200
    assert response.json() == "null"







def test_delete_log():
    response = client.delete("/delete/2")
    assert response.status_code == 200
    assert response.json() =={}



