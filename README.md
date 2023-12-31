## KULLANILAN TASARIM KALIPLARI
Bütün sistem için <b>api gateway</b> yapısı ve her bir mikroservis için <b>application factory pattern</b> kullandım.
## Mikroservislerin dökümanları
kullanıcı servisinin dökümantasyonu:http://0.0.0.0:5002/docs

apigateway servisinin dökümantasysonu:http://0.0.0.0:5003/docs

log servisinin dökümantasyonu:http://0.0.0.0:5004/docs

## Log servisinin kaynakçası
Önceden hazırladığım bir log servisini loglama için kullandım.Session loglar yerine çeşitli logları barındıran bir servis hazırladım.
https://github.com/SirmaXX/Log_manager
## Proje Nasıl Çalıştırılır
Aşağıdaki  komutları yazarak projeyi çalıştırabilirsiniz.

1. sudo docker-compose up --build

2. sudo make all  

# Postman verisine nasıl erişilir
DenemeJsonCollection.postman_collection.json'ı postman'e entegre ederek kullanabilirsiniz

# Testler nasıl çalıştırılır
Servislerdeki test_main.py  dosyalarını
Aşağıdaki komut satırlarını sıra ile yazarak,backend servisi containerına erişerek unit testleri çalıştırabilirsiniz.

sudo docker exec -it "servismi" /bin/bash

pytest


### ip whitelist  örneği 
https://github.com/SirmaXX/fastapi-micro/blob/main/ApiGateway/app/main.py#L24

## rate limit örneği

https://github.com/SirmaXX/fastapi-micro/blob/main/ApiGateway/app/Routers/restapi.py#L31

## tokenizasyon örneği 
kullanıcı servisi
https://github.com/SirmaXX/fastapi-micro/blob/main/User_Service/app/Routers/users.py#L232

apigateway
https://github.com/SirmaXX/fastapi-micro/blob/main/ApiGateway/app/Routers/restapi.py#L91

## Kaynakça

https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
https://github.com/baranbartu/microservices-with-fastapi
https://www.youtube.com/watch?v=6hTRw_HK3Ts
https://stackoverflow.com/questions/66867814/fastapi-how-to-allow-endpoint-access-for-specific-ip-only

## Eksiklikler