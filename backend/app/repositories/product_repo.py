import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.product import ProductFamily, ProductVersion, ProductCertificate, ProductPassport

def list_product_families(db: Session) -> List[ProductFamily]:
    """List all product families with their latest versions and certificates."""
    stmt = (
        select(ProductFamily)
        .options(
            joinedload(ProductFamily.versions).joinedload(ProductVersion.certificates),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.passports)
        )
        .order_by(ProductFamily.created_at.desc())
    )
    return list(db.execute(stmt).unique().scalars().all())

def get_product_family(db: Session, family_id: uuid.UUID) -> Optional[ProductFamily]:
    """Retrieve single product family by ID."""
    stmt = (
        select(ProductFamily)
        .options(
            joinedload(ProductFamily.versions).joinedload(ProductVersion.certificates),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.passports)
        )
        .where(ProductFamily.id == family_id)
    )
    return db.execute(stmt).unique().scalar_one_or_none()

def create_product_family(db: Session, data: Dict[str, Any]) -> ProductFamily:
    """Create a new product family."""
    family = ProductFamily(
        name=data["name"],
        category=data.get("category", "Finished Leather"),
        hs_code=data.get("hs_code", "4107"),
        itc_hs_code=data.get("itc_hs_code", "4107.12.00"),
        leather_type=data.get("leather_type", "Bovine Full Grain"),
        description=data.get("description")
    )
    db.add(family)
    db.commit()
    db.refresh(family)

    # Automatically create initial Version 1.0
    initial_version = ProductVersion(
        product_family_id=family.id,
        version_tag="v1.0",
        materials=data.get("materials", ["Bovine hide"]),
        finishes=data.get("finishes", ["Semi-aniline"]),
        thickness_range_mm=data.get("thickness_range_mm", ["1.2-1.4"]),
        monthly_capacity_sqft=data.get("monthly_capacity_sqft", 25000),
        moq_sqft=data.get("moq_sqft", 2000),
        lead_time_days=data.get("lead_time_days", 30),
        price_basis_inr=data.get("price_basis_inr", 280.0),
        price_basis_usd=data.get("price_basis_usd", 3.35),
        status="approved"
    )
    db.add(initial_version)
    db.commit()
    db.refresh(initial_version)

    # Generate Digital Product Passport
    passport = ProductPassport(
        product_version_id=initial_version.id,
        passport_number=f"DPP-IN-{uuid.uuid4().hex[:8].upper()}",
        status="active"
    )
    db.add(passport)
    db.commit()
    db.refresh(family)

    return get_product_family(db, family.id)

def add_product_version(db: Session, family_id: uuid.UUID, version_data: Dict[str, Any]) -> ProductVersion:
    """Create a new version for an existing product family."""
    version = ProductVersion(
        product_family_id=family_id,
        version_tag=version_data.get("version_tag", "v1.1"),
        materials=version_data.get("materials", []),
        finishes=version_data.get("finishes", []),
        thickness_range_mm=version_data.get("thickness_range_mm", []),
        monthly_capacity_sqft=version_data.get("monthly_capacity_sqft", 25000),
        moq_sqft=version_data.get("moq_sqft", 2000),
        lead_time_days=version_data.get("lead_time_days", 30),
        price_basis_inr=version_data.get("price_basis_inr", 280.0),
        price_basis_usd=version_data.get("price_basis_usd", 3.35),
        status="pending_review"
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version

def add_product_certificate(db: Session, version_id: uuid.UUID, cert_data: Dict[str, Any]) -> ProductCertificate:
    """Attach a verified lab test or compliance certificate to a product version."""
    cert = ProductCertificate(
        product_version_id=version_id,
        cert_type=cert_data["cert_type"],
        certificate_name=cert_data["certificate_name"],
        issuer=cert_data["issuer"],
        accredited_lab=cert_data.get("accredited_lab", "Eurofins / TÜV Rheinland"),
        scope=cert_data.get("scope"),
        file_hash=cert_data.get("file_hash"),
        issue_date=cert_data["issue_date"],
        expiry_date=cert_data.get("expiry_date"),
        status=cert_data.get("status", "verified")
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

def get_product_passport(db: Session, version_id: uuid.UUID) -> Optional[ProductPassport]:
    """Retrieve Digital Product Passport for a product version."""
    stmt = (
        select(ProductPassport)
        .options(
            joinedload(ProductPassport.version).joinedload(ProductVersion.family),
            joinedload(ProductPassport.version).joinedload(ProductVersion.certificates)
        )
        .where(ProductPassport.product_version_id == version_id)
    )
    return db.execute(stmt).unique().scalar_one_or_none()
