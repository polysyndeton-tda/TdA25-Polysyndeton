FROM node:18-alpine as frontend-build
WORKDIR /app/frontend

COPY frontend/ .

RUN npm install
RUN npm run build

FROM python:3.10-slim
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ backend/
COPY --from=frontend-build /app/frontend/build /app/backend/static

EXPOSE 5000
#For making Flask not ignore print from @app.route
# https://stackoverflow.com/a/57254931/11844784 from https://stackoverflow.com/questions/32550487/how-to-print-from-flask-app-route-to-python-console
ENV PYTHONUNBUFFERED=1
CMD ["python", "backend/main.py"]
