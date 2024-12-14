cd frontend
npm install
npm run build

cd ../backend
pip install --no-cache-dir -r requirements.txt --break-system-packages

python app.py
