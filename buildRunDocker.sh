sudo docker build --no-cache -t tda-app .
sudo docker run -p 5000:5000 tda-app