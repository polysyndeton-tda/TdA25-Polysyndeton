# Stop all running containers, suppress errors if none exist
running_containers=$(sudo docker ps -q)
if [ ! -z "$running_containers" ]; then
    sudo docker stop $running_containers
else
    echo "No running containers to stop"
fi

# Remove existing images
sudo docker rmi tda-app -f

# Clear build cache
# If I understand correctly, only needed from time to time if I wanted to reclaim some used space on the drive
# This is where the cache is. 
#Cache shouldn't be evil (according to next comment = when there are file changes, docker should be able to update on its own)
# => without forcing deleting it every time
# sudo docker builder prune -f

# Build with no cache and pull latest base images
# If the primary concern is updating the files from your development folder and the rest of the Docker setup remains unchanged, 
#you might not need to use --no-cache for every build.
# Docker will rebuild the layers that have changed, so if only the files in your development folder have been updated,
# Docker should detect those changes and only rebuild the relevant layers.

sudo docker build -t tda-app . #--pull --no-cache (that is not necessary I think)
sudo docker run -p 5000:5000 tda-app
