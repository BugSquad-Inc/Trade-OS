from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import health, capability, matches, signals, accounts, outreach, ingest, search, agents, customs, crm

app = FastAPI(
    title="Trade OS API",
    description="Export Revenue Operating System — Leather & Materials Vertical",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health.router)
app.include_router(capability.router)
app.include_router(matches.router)
app.include_router(signals.router)
app.include_router(accounts.router)
app.include_router(outreach.router)
app.include_router(ingest.router)
app.include_router(search.router)
app.include_router(agents.router)
app.include_router(customs.router)
app.include_router(crm.router)

@app.get("/")
def root():
    return {
        "name": "Trade OS API",
        "status": "running",
        "docs": "/docs",
        "vertical": "Leather & Materials Exporters"
    }
