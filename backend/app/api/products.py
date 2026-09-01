import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key, get_current_tenant, require_role
from app.models.tenant import Tenant, UserRole
from app.schemas.product import (
    ProductFamilyCreate,
    ProductFamilyResponse,
    ProductVersionCreate,
    ProductVersionResponse,
    ProductCertificateCreate,
    ProductCertificateResponse,
    ProductPassportResponse
)
from app.repositories import product_repo

router = APIRouter(prefix="/api/v1/products", tags=["Product Passports & Matrix"])

@router.get("/dpp/public/{public_token}", response_model=ProductPassportResponse)
def get_public_dpp(public_token: str, db: Session = Depends(get_db)):
    """
    Public unauthenticated endpoint for EU buyers scanning DPP QR codes.
    Returns verified chemical tests, origin coordinates, and carbon footprint.
    """
    passport = product_repo.get_public_product_passport(db, public_token)
    if not passport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Product Passport token not found or expired.")
    return passport

@router.get("", response_model=List[ProductFamilyResponse], dependencies=[Depends(require_api_key)])
def list_products(
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    """List all registered product families with version histories, physical specs, chemical tests, and DPPs."""
    return product_repo.list_product_families(db, tenant_id=tenant.id)

@router.post("", response_model=ProductFamilyResponse, dependencies=[Depends(require_api_key), Depends(require_role([UserRole.owner, UserRole.sales, UserRole.compliance]))])
def create_product(
    product_in: ProductFamilyCreate,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    """Register a new product article family with full specification matrix and Digital Passport."""
    data = product_in.model_dump()
    return product_repo.create_product_family(db, data, tenant_id=tenant.id)

@router.get("/{family_id}", response_model=ProductFamilyResponse, dependencies=[Depends(require_api_key)])
def get_product(
    family_id: uuid.UUID,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    """Retrieve single product family by ID."""
    family = product_repo.get_product_family(db, family_id, tenant_id=tenant.id)
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product family not found.")
    return family

@router.post("/{family_id}/versions", response_model=ProductVersionResponse, dependencies=[Depends(require_api_key), Depends(require_role([UserRole.owner, UserRole.compliance]))])
def create_version(
    family_id: uuid.UUID,
    version_in: ProductVersionCreate,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    """Create a new version for an existing product family."""
    family = product_repo.get_product_family(db, family_id, tenant_id=tenant.id)
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product family not found.")
    return product_repo.add_product_version(db, family_id, version_in.model_dump())

@router.post("/versions/{version_id}/certificates", response_model=ProductCertificateResponse, dependencies=[Depends(require_api_key), Depends(require_role([UserRole.owner, UserRole.compliance, UserRole.analyst]))])
def attach_certificate(
    version_id: uuid.UUID,
    cert_in: ProductCertificateCreate,
    db: Session = Depends(get_db)
):
    """Attach verified lab test certificate (LWG, REACH, Chromium VI) to a product version."""
    return product_repo.add_product_certificate(db, version_id, cert_in.model_dump())

@router.get("/versions/{version_id}/passport", response_model=ProductPassportResponse, dependencies=[Depends(require_api_key)])
def get_passport(version_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve verified Digital Product Passport (DPP) with QR/traceability metadata."""
    passport = product_repo.get_product_passport(db, version_id)
    if not passport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product passport not found for this version.")
    return passport
