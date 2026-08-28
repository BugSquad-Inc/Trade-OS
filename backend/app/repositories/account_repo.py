from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from typing import List, Optional
import uuid
from app.models.company import EntityCompany, EntityPerson, EntityProduct
from app.models.compliance import EntityCertification

def get_all_buyers(db: Session) -> List[EntityCompany]:
    stmt = select(EntityCompany).where(EntityCompany.country_code != "IN").order_by(EntityCompany.canonical_name)
    return list(db.execute(stmt).scalars().all())

def get_company_by_id(db: Session, company_id: uuid.UUID) -> Optional[EntityCompany]:
    stmt = (
        select(EntityCompany)
        .where(EntityCompany.id == company_id)
        .options(
            joinedload(EntityCompany.persons),
            joinedload(EntityCompany.products),
            joinedload(EntityCompany.certifications),
            joinedload(EntityCompany.signals)
        )
    )
    return db.execute(stmt).unique().scalar_one_or_none()

def get_company_by_name(db: Session, name: str) -> Optional[EntityCompany]:
    stmt = select(EntityCompany).where(EntityCompany.canonical_name == name)
    return db.execute(stmt).scalar_one_or_none()

def get_contacts_for_company(db: Session, company_id: uuid.UUID) -> List[EntityPerson]:
    stmt = select(EntityPerson).where(EntityPerson.company_id == company_id).order_by(EntityPerson.is_primary.desc(), EntityPerson.confidence.desc())
    return list(db.execute(stmt).scalars().all())
