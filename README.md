## To start the application, the user should use the following docker commands:
* "docker build -t p1 ." to build your image
* "docker run -p 5001:5000 p1" to get a container running
* Now that the container is running, go to "localhost:5001" to view the home page and navigate from there
## To stop the application, the user should use the following docker commands:
* "docker ps" to view the running container
* "docker stop container_id", where container_id is the CONTAINER ID listed when using docker ps
* "docker rm container_id", where container_id is the CONTAINER ID listed when using docker ps
* "docker images" to view the running image
* "docker image rm image_id", where image_id is the IMAGE ID listed when running "docker images"

<!-- Will look into making a docker compose file so that the user can just run docker-compose up to build and run everything needed>