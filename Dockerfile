FROM node:18-alpine as frontend-build
WORKDIR /app/frontend

ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}
ENV SECRET_KEY=${SECRET_KEY}
ENV SUPERUSER_NAME=${SUPERUSER_USERNAME}
ENV SUPERUSER_EMAIL=${SUPERUSER_EMAIl}
ENV SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD}

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
CMD ["python", "backend/main.py"]
