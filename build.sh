 #!/bin/bash
docker-compose -f docker-compose.yml down
docker rmi securityframework_sec-fw-mysql
docker rmi securityframework_sec-fw-frontend
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up --force-recreate
