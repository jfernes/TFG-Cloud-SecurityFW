 #!/bin/bash
docker-compose -f docker-compose.yml down
docker rmi securityframework_mysql
docker rmi securityframework_frontend
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up --force-recreate
