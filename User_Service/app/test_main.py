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

#KULLANICI BÖLÜMÜNÜN TESTLERİ
def test_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {}

postuser={
  "username": "postuser1",
  "password": "deneme123"
}

def test_post_user():
    response = client.post("/users/add", json=postuser)
    assert response.status_code == 200
    assert response.json() == {}




def test_update_user():
    response = client.put("/users/2", json = {
    "id": 2,
    "username": "postuser123",
    "password": "son123"
  })
    assert response.status_code == 200
    assert response.json() == "string"




def test_delete_users():
    response = client.delete("/users/delete/10")
    assert response.status_code == 200
    assert response.json() =={}


#CİHAZ BÖLÜMÜNÜN TESTLERİ
dataset  = [
  {
    "device_name": "string",
    "active": True,
    "macaddress": "string",
    "id": 2,
    "ipaddress": "string"
  },
  {
    "device_name": "deneme",
    "active": True,
    "macaddress": "12:c2:KK:33",
    "id": 4,
    "ipaddress": "sea-97@hotmail.com"
  },
  {
    "device_name": "sondenemeupload11",
    "active": True,
    "macaddress": "12:c2:12:33",
    "id": 3,
    "ipaddress": "192.168.2.1"
  }
]
def test_devices():
    response = client.get("/devices/")
    assert response.status_code == 200
    assert response.json() == dataset 



postuser={
  "username": "postuser1",
  "password": "deneme123"
}

def test_post_device():
    response = client.post("/devices/add", json=postuser)
    assert response.status_code == 200
    assert response.json() == {}




def test_update_device():
    response = client.put("/devices/update/2/deneme", json = {
    "id": 2,
    "username": "postuser123",
    "password": "son123"
  })
    assert response.status_code == 200
    assert response.json() == "string"




def test_delete_device():
    response = client.delete("/devices/delete/10")
    assert response.status_code == 200
    assert response.json() =={}


#ŞİRKET BÖLÜMÜNÜN TESTLERİ



def test_companies():
    response = client.get("/companies/")
    assert response.status_code == 200
    assert response.json() == {
  "mesaj": "şirket yok"
}





postcompany={
  "Company_name": "string",
  "DevicesCount": 0,
  "Email": "string"
}

def test_post_company():
    response = client.post("/companies/add", json=postcompany)
    assert response.status_code == 200
    assert response.json() == {}




def test_update_company():
    response = client.put("/companies/update/2/deneme", json = {
    "id": 2,
    "username": "postuser123",
    "password": "son123"
  })
    assert response.status_code == 200
    assert response.json() == "string"




def test_delete_company():
    response = client.delete("/companies/delete/4")
    assert response.status_code == 200
    assert response.json() =={}