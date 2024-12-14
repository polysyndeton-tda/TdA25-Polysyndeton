# Build frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# Build backend and combine
FROM python:3.10-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ backend/

# Copy frontend build to backend static
COPY --from=frontend-build /app/frontend/dist backend/static

EXPOSE 5000
CMD ["python", "backend/app.py"]
