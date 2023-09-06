## mikroservislerin dökümanları
müşteri servisinin dökümantasyonu:http://0.0.0.0:5001/docs
kullanıcı servisinin dökümantasyonu:http://0.0.0.0:5002/docs
apigateway servisinin dökümantasysonu:http://0.0.0.0:5003/docs
log servisinin dökümantasyonu:http://0.0.0.0:5004/docs
### tabloların oluşturulması

sudo docker exec -it db /bin/bash


psql -h localhost -U postgres


CREATE DATABASE costumers;
CREATE DATABASE users;