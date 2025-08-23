#!/bin/bash
# Setup trap to kill background processes on script exit 
#(to ma pry ukoncit npm run dev spusteny na pozadi, ktery by jinak ctrl c neukoncil a pry by bylo potreba pkill -f "npm run dev" 
# Function to kill background processes
cleanup() {
    echo "Cleaning up..."

    #sometimes they do kill processes..
    npx kill-port 5173
    npx kill-port 5000
    
    pkill -P $$
}

# Setup trap to execute cleanup function on script exit
trap cleanup EXIT

cd frontend
npm install
rm -rf ./build/ #clear the build folder to be sure there are no files from the previous build

# Backup original .env if it exists
# [ -f .env ] && cp .env .env.backup

# Create temporary .env
echo "PUBLIC_API_BASE_URL=http://localhost:5000/api/v1" > .env

npm run dev & #& means run in background

echo $(pwd)
rm -rf ../backend/static/* #same with the backend static folder (there were issues before)
cp -a /build/. ../backend/static

#Restore doesn't work - the frontend somehow picks up on it (probably live reload)
#So instead modify .env here and modify it in buildRunDocker.sh)

# Restore original .env
# [ -f .env.backup ] && mv .env.backup .env

cd ../backend
pip install --no-cache-dir -r requirements.txt --break-system-packages

python3 main.py