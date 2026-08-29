import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
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

router = APIRouter(prefix="/api/v1/products", tags=["Product Passports & Catalog"], dependencies=[Depends(require_api_key)])

@router.get("", response_model=List[ProductFamilyResponse])
def list_products(db: Session = Depends(get_db)):
    """List all registered product families with version histories and compliance certificates."""
    return product_repo.list_product_families(db)

@router.post("", response_model=ProductFamilyResponse)
def create_product(product_in: ProductFamilyCreate, db: Session = Depends(get_db)):
    """Register a new product family and automatically initialize Version 1.0 with Digital Passport."""
    data = product_in.model_dump()
    return product_repo.create_product_family(db, data)

@router.get("/{family_id}", response_model=ProductFamilyResponse)
def get_product(family_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve single product family by ID."""
    family = product_repo.get_product_family(db, family_id)
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product family not found.")
    return family

@router.post("/{family_id}/versions", response_model=ProductVersionResponse)
def create_version(family_id: uuid.UUID, version_in: ProductVersionCreate, db: Session = Depends(get_db)):
    """Create a new version for an existing product family."""
    family = product_repo.get_product_family(db, family_id)
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product family not found.")
    return product_repo.add_product_version(db, family_id, version_in.model_dump())

@router.post("/versions/{version_id}/certificates", response_model=ProductCertificateResponse)
def attach_certificate(version_id: uuid.UUID, cert_in: ProductCertificateCreate, db: Session = Depends(get_db)):
    """Attach verified lab test certificate (LWG, REACH, Chromium VI) to a product version."""
    return product_repo.add_product_certificate(db, version_id, cert_in.model_dump())

@router.get("/versions/{version_id}/passport", response_model=ProductPassportResponse)
def get_passport(version_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve verified Digital Product Passport (DPP) with QR/traceability metadata."""
    passport = product_repo.get_product_passport(db, version_id)
    if not passport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product passport not found for this version.")
    return passport
