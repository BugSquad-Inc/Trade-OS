import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_
from app.models.product import (
    ProductFamily,
    ProductVersion,
    ProductSpecification,
    ChemicalComplianceSpec,
    TraceabilitySpec,
    ProductCertificate,
    ProductPassport
)

def list_product_families(db: Session, tenant_id: Optional[uuid.UUID] = None) -> List[ProductFamily]:
    """List all product families with their latest versions, physical specs, chemical specs, and certificates."""
    stmt = (
        select(ProductFamily)
        .options(
            joinedload(ProductFamily.versions).joinedload(ProductVersion.specifications),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.chemical_spec),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.traceability_spec),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.certificates),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.passports)
        )
        .order_by(ProductFamily.created_at.desc())
    )
    if tenant_id:
        stmt = stmt.where(or_(ProductFamily.tenant_id == tenant_id, ProductFamily.tenant_id.is_(None)))
    return list(db.execute(stmt).unique().scalars().all())

def get_product_family(db: Session, family_id: uuid.UUID, tenant_id: Optional[uuid.UUID] = None) -> Optional[ProductFamily]:
    """Retrieve single product family by ID with multi-tenant check."""
    stmt = (
        select(ProductFamily)
        .options(
            joinedload(ProductFamily.versions).joinedload(ProductVersion.specifications),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.chemical_spec),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.traceability_spec),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.certificates),
            joinedload(ProductFamily.versions).joinedload(ProductVersion.passports)
        )
        .where(ProductFamily.id == family_id)
    )
    if tenant_id:
        stmt = stmt.where(or_(ProductFamily.tenant_id == tenant_id, ProductFamily.tenant_id.is_(None)))
    return db.execute(stmt).unique().scalar_one_or_none()

def create_product_family(db: Session, data: Dict[str, Any], tenant_id: Optional[uuid.UUID] = None) -> ProductFamily:
    """Create a new product family with full specification matrix and DPP record."""
    family = ProductFamily(
        tenant_id=tenant_id,
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
        materials=data.get("materials", ["European Rawhide", "Vegetable Tanning Extracts"]),
        finishes=data.get("finishes", ["Semi-aniline", "Waxed pull-up"]),
        thickness_range_mm=data.get("thickness_range_mm", ["1.2-1.4"]),
        monthly_capacity_sqft=data.get("monthly_capacity_sqft", 25000),
        moq_sqft=data.get("moq_sqft", 2000),
        lead_time_days=data.get("lead_time_days", 30),
        sample_lead_time_days=7,
        price_basis_inr=data.get("price_basis_inr", 280.0),
        price_basis_usd=data.get("price_basis_usd", 3.35),
        status="approved"
    )
    db.add(initial_version)
    db.commit()
    db.refresh(initial_version)

    # Physical Specifications
    spec_data = data.get("specifications") or {}
    spec = ProductSpecification(
        product_version_id=initial_version.id,
        thickness_min_mm=spec_data.get("thickness_min_mm", 1.2),
        thickness_max_mm=spec_data.get("thickness_max_mm", 1.4),
        temper=spec_data.get("temper", "medium_soft"),
        tensile_strength_n_per_mm2=spec_data.get("tensile_strength_n_per_mm2", 15.0),
        tear_strength_n=spec_data.get("tear_strength_n", 40.0),
        grain_type=spec_data.get("grain_type", "Full Grain Natural Mill"),
        tannage_type=spec_data.get("tannage_type", "Chrome-Free Synthetic / Veg Retan"),
        origin_country=spec_data.get("origin_country", "India")
    )
    db.add(spec)

    # Chemical Compliance Limits
    chem_data = data.get("chemical_spec") or {}
    chem = ChemicalComplianceSpec(
        product_version_id=initial_version.id,
        chromium_vi_ppm=chem_data.get("chromium_vi_ppm", 0.0),
        azo_dyes_ppm=chem_data.get("azo_dyes_ppm", 0.0),
        formaldehyde_ppm=chem_data.get("formaldehyde_ppm", 12.0),
        pfas_free=chem_data.get("pfas_free", True),
        reach_svhc_status=chem_data.get("reach_svhc_status", "compliant"),
        lab_test_report_id=chem_data.get("lab_test_report_id", "TR-TUV-2026-8812"),
        accredited_lab=chem_data.get("accredited_lab", "TÜV Rheinland / Eurofins")
    )
    db.add(chem)

    # Traceability & EUDR Coordinates
    trace_data = data.get("traceability_spec") or {}
    trace = TraceabilitySpec(
        product_version_id=initial_version.id,
        abattoir_license_no=trace_data.get("abattoir_license_no", "APEDA-TN-7821"),
        mandal_district=trace_data.get("mandal_district", "Ambur / Tirupattur District"),
        state=trace_data.get("state", "Tamil Nadu"),
        geolocation_lat=trace_data.get("geolocation_lat", 12.7904),
        geolocation_lng=trace_data.get("geolocation_lng", 78.7163),
        eudr_cutoff_cleared=trace_data.get("eudr_cutoff_cleared", True),
        hide_origin_batch=trace_data.get("hide_origin_batch", "BATCH-2026-TN-04")
    )
    db.add(trace)

    # Generate Digital Product Passport
    passport = ProductPassport(
        product_version_id=initial_version.id,
        passport_number=f"DPP-IN-{uuid.uuid4().hex[:8].upper()}",
        public_token=f"tok_{uuid.uuid4().hex[:16]}",
        carbon_footprint_kg_co2e=4.2,
        status="active"
    )
    db.add(passport)
    db.commit()
    db.refresh(family)

    return get_product_family(db, family.id, tenant_id=tenant_id)

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
        status="approved"
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
            joinedload(ProductPassport.version).joinedload(ProductVersion.specifications),
            joinedload(ProductPassport.version).joinedload(ProductVersion.chemical_spec),
            joinedload(ProductPassport.version).joinedload(ProductVersion.traceability_spec),
            joinedload(ProductPassport.version).joinedload(ProductVersion.certificates)
        )
        .where(ProductPassport.product_version_id == version_id)
    )
    return db.execute(stmt).unique().scalar_one_or_none()

def get_public_product_passport(db: Session, public_token: str) -> Optional[ProductPassport]:
    """Retrieve public DPP by secure token without authentication."""
    stmt = (
        select(ProductPassport)
        .options(
            joinedload(ProductPassport.version).joinedload(ProductVersion.family),
            joinedload(ProductPassport.version).joinedload(ProductVersion.specifications),
            joinedload(ProductPassport.version).joinedload(ProductVersion.chemical_spec),
            joinedload(ProductPassport.version).joinedload(ProductVersion.traceability_spec),
            joinedload(ProductPassport.version).joinedload(ProductVersion.certificates)
        )
        .where(ProductPassport.public_token == public_token)
    )
    return db.execute(stmt).unique().scalar_one_or_none()
