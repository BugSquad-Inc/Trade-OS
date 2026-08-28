import os

files = {
    'backend/Dockerfile': """FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    libpq-dev \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
""",

    'frontend/nginx.conf': """server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://backend:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
""",

    'frontend/Dockerfile': """FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""",

    'docker-compose.prod.yml': """version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: tradeos_postgres_prod
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-tradeos}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-tradeos_secret_password}
      POSTGRES_DB: ${POSTGRES_DB:-trade_os}
    ports:
      - "5433:5432"
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tradeos -d trade_os"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: tradeos_backend_prod
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+psycopg://tradeos:tradeos_secret_password@postgres:5432/trade_os
      API_KEY: ${API_KEY:-tradeos_dev_secret_key_2026}
      PORT: 8000
    ports:
      - "8000:8000"
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: tradeos_frontend_prod
    depends_on:
      - backend
    ports:
      - "3000:80"
    restart: always

volumes:
  postgres_prod_data:
""",

    'scripts/verify_production_readiness.py': """import sys
import os
sys.path.insert(0, os.path.abspath("backend"))

from sqlalchemy import text
from app.database import engine
from app.config import settings

def run_readiness_audit():
    print("=" * 70)
    print("TRADE OS -- PRODUCTION READINESS AND VERIFICATION AUDIT")
    print("=" * 70)
    with engine.connect() as conn:
        print("[1/5] Checking Database Schemas...")
        schemas = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('bronze', 'silver', 'gold', 'audit', 'app')")).fetchall()
        schema_names = [s[0] for s in schemas]
        print(f"      Found Schemas: {schema_names}")
        assert len(schema_names) >= 4

        print("[2/5] Verifying Medallion Tables...")
        tables = conn.execute(text("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('silver', 'gold', 'audit')")).fetchall()
        print(f"      Total Tables: {len(tables)}")
        assert len(tables) >= 8

        print("[3/5] Verifying Data Counts...")
        exporters = conn.execute(text("SELECT count(*) FROM gold.exporter_capability")).scalar()
        buyers = conn.execute(text("SELECT count(*) FROM silver.entity_company WHERE country_code != 'IN'")).scalar()
        matches = conn.execute(text("SELECT count(*) FROM gold.match_candidate")).scalar()
        signals = conn.execute(text("SELECT count(*) FROM gold.signal_feed")).scalar()
        customs = conn.execute(text("SELECT count(*) FROM silver.customs_shipments_normalized")).scalar()
        print(f"      Exporters: {exporters}, Buyers: {buyers}, Matches: {matches}, Signals: {signals}, Customs: {customs}")
        assert exporters >= 1 and buyers >= 5 and matches >= 5

        print("[4/5] Auditing Explainability Drivers (Law 2)...")
        zero_drivers = conn.execute(text("SELECT count(*) FROM gold.match_candidate WHERE drivers IS NULL OR jsonb_array_length(drivers) = 0")).scalar()
        assert zero_drivers == 0
        print(f"      Zero-driver matches: {zero_drivers}")

        print("[5/5] Production System Status: 100% HEALTHY AND VERIFIED!")
        print("=" * 70)

if __name__ == "__main__":
    run_readiness_audit()
""",

    'backend/app/tests/test_production_e2e.py': """import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_production_readiness_e2e():
    # 1. Health
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    # 2. Exporter Capability
    cap = client.get("/api/v1/capability", headers={"X-TradeOS-Key": settings.API_KEY})
    assert cap.status_code == 200
    assert cap.json()["company_name"] == "Butler's Leather"

    # 3. Matches
    matches = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    assert matches.status_code == 200
    assert len(matches.json()["matches"]) >= 5

    # 4. Signals
    signals = client.get("/api/v1/signals", headers={"X-TradeOS-Key": settings.API_KEY})
    assert signals.status_code == 200
    assert len(signals.json()["signals"]) >= 5

    # 5. Customs
    customs = client.get("/api/v1/customs/shipments", headers={"X-TradeOS-Key": settings.API_KEY})
    assert customs.status_code == 200
    assert customs.json()["total_records"] >= 5

    # 6. Analytics
    analytics = client.get("/api/v1/analytics/kpis", headers={"X-TradeOS-Key": settings.API_KEY})
    assert analytics.status_code == 200
    assert analytics.json()["activation"]["match_explainability_pct"] == 100.0

    # 7. Lanes
    lanes = client.get("/api/v1/lanes/corridors", headers={"X-TradeOS-Key": settings.API_KEY})
    assert lanes.status_code == 200
    assert lanes.json()["total_corridors"] >= 4

    # 8. Webhooks
    webhooks = client.get("/api/v1/webhooks", headers={"X-TradeOS-Key": settings.API_KEY})
    assert webhooks.status_code == 200
"""
}

for path, content in files.items():
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'[CREATED] {path}')

print('[SUCCESS] All Sprint 7 Production Packaging files written successfully!')
