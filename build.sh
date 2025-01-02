cd frontend
npm install
npm run build

cd ../backend
pip install --no-cache-dir -r requirements.txt --break-system-packages

export FLASK_APP=main.py
flask run
