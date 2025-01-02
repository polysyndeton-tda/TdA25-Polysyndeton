FROM node:18-alpine as frontend-build
WORKDIR /app/frontend

COPY frontend/ .

RUN npm install
RUN npm run build

FROM python:3.10-slim
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY --from=frontend-build /app/frontend/dist /app/backend/static

EXPOSE 5000
CMD ["python", "backend/main.py"]