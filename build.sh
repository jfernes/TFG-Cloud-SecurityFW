docker-compose -f docker-compose.yml down
docker rmi sec-fw-frontend
docker rmi sec-fw-mysql
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up --force-recreate
