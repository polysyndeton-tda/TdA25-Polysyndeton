# echo $(pwd)
# remove artefacts from previous build https://askubuntu.com/questions/60228/how-to-remove-all-files-from-a-directory
# only if directory is not empty (if it exists and is empty, we get rm: cannot remove './backend/src/static/*': No such file or directory)
if [ -d "./backend/src/static" ] && [ "$(ls -A ./backend/src/static)" ]; then
    rm -r ./backend/src/static/*
fi

cd frontend
npm install
npm run build

echo $(pwd)
cp -a ./build/. ../backend/src/static

cd ../backend
pip install --no-cache-dir -r requirements.txt --break-system-packages

export FLASK_APP=main.py
flask run