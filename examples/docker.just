# Build a Docker image
build image_tag:
    docker build -t {{image_tag}} .

# Run a container in detached mode
run name image_tag host_port="8080" container_port="8080":
    docker run -d -p {{host_port}}:{{container_port}} --name {{name}} {{image_tag}}

# Run a container interactively with a shell
shell image_tag:
    docker run --rm -it --entrypoint bash {{image_tag}}

# Tail container logs
logs name:
    docker logs -f {{name}}

# Stop and remove a container
stop name:
    docker stop {{name}} && docker rm {{name}}

# Remove all unused Docker data
prune:
    docker system prune -af

# List all containers
ps:
    docker ps -a

# List all images
images:
    docker images
