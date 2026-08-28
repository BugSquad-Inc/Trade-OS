import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. docker-compose.yml
w("docker-compose.yml", """version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: trade_os_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: tradeos
      POSTGRES_PASSWORD: tradeos_secret_password
      POSTGRES_DB: trade_os
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tradeos -d trade_os"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    name: trade_os_postgres_data
""")

# 2. backend/Dockerfile
w("backend/Dockerfile", """FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
""")

# 3. .env & .env.example
env_content = """ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://tradeos:tradeos_secret_password@localhost:5433/trade_os
API_KEY=tradeos_pilot_secret_key_2026
OPENAI_API_KEY=mock_key
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
PORT=8000
"""
w(".env", env_content)
w(".env.example", env_content)

# 4. backend/requirements.txt
w("backend/requirements.txt", """fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
sqlalchemy>=2.0.28
psycopg[binary]>=3.1.18
asyncpg>=0.29.0
python-dotenv>=1.0.1
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
pgvector>=0.2.5
""")

# 5. backend/app/config.py
w("backend/app/config.py", """import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+psycopg://tradeos:tradeos_secret_password@localhost:5433/trade_os"
    API_KEY: str = "tradeos_pilot_secret_key_2026"
    OPENAI_API_KEY: str = "mock_key"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
    PORT: int = 8000

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
""")

# 6. backend/app/database.py
w("backend/app/database.py", """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

# 7. backend/app/api/deps.py
w("backend/app/api/deps.py", """from fastapi import Header, HTTPException, status
from app.config import settings

async def require_api_key(x_tradeos_key: str = Header(..., alias="X-TradeOS-Key")):
    if x_tradeos_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TradeOS-Key authentication header."
        )
    return x_tradeos_key
""")

# 8. backend/app/schemas/health.py
w("backend/app/schemas/health.py", """from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str = "ok"
    environment: str
    database: str
    version: str = "1.0.0"
""")

# 9. backend/app/api/health.py
w("backend/app/api/health.py", """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.config import settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/api/v1/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unreachable: {str(e)}"

    return HealthResponse(
        status="ok",
        environment=settings.ENVIRONMENT,
        database=db_status,
        version="1.0.0"
    )
""")

print("[SUCCESS] Part 1 (Infrastructure) built successfully")
