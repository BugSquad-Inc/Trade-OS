from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.api import (
    health, capability, matches, signals, accounts, outreach, ingest,
    search, agents, customs, crm, analytics, webhooks, lanes,
    websocket, exporters, products, verification, deals, today,
    tenants, users, documents, shipments, audit, journey
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-TradeOS-Engine"] = "v2.0-universal-sprint7"
        return response

app = FastAPI(
    title="Trade OS API",
    description="Export Revenue Operating System — Universal Multi-Tenant Architecture",
    version="2.0.0"
)

# Security & Performance Middlewares
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include All 26 Production API Routers
app.include_router(health.router)
app.include_router(journey.router)
app.include_router(today.router)
app.include_router(deals.router)
app.include_router(documents.router)
app.include_router(shipments.router)
app.include_router(audit.router)
app.include_router(tenants.router)
app.include_router(users.router)
app.include_router(exporters.router)
app.include_router(products.router)
app.include_router(verification.router)
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
app.include_router(analytics.router)
app.include_router(webhooks.router)
app.include_router(lanes.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {
        "name": "Trade OS API",
        "status": "running",
        "version": "2.0.0",
        "docs": "/docs",
        "vertical": "Indian SMB Leather & Universal Materials Exporters"
    }
