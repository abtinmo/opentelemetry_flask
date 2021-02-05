# opentelemetry_flask


    git clone https://github.com/abtinmo/opentelemetry_flask/
  
    cd opentelemetry_flask/
  
    docker-compose up -d
  
  
  send login request with:
  
      curl --request POST \
      --url http://localhost:5000/login \
      --header 'Content-Type: application/json' \
      --data '{
      "username": "abtin"
    }'
    
    
 send verify request with code from previous request:
 
     curl --request POST \
      --url http://localhost:5000/verify \
      --header 'Content-Type: application/json' \
      --data '{
      "username": "abtin",
      "code": "****"
    }'
    
 open http://localhost:16686/ and see the result
