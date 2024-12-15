build:
	docker build -t tda-app .

run:
	docker run -p 5000:5000 tda-app
