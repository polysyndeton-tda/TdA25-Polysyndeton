cd frontend
npm install
npm run build

cd ../backend
pip install --no-cache-dir -r requirements.txt --break-system-packages

rm -rf static
mkdir static
cp -r  ../frontend/dist/* static

python app.py
