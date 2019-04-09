run in dev mode
docker-compose up

connect to localhost:8080

build the static files
docker-compose exec -u 1000 node /build.sh

