docker rm -f  web-api
docker build -t web-api .
docker run -d --name web-api -p 8010:8010 web-api
