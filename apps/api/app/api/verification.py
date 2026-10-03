from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api.app.core.database import get_db
from apps.api.app.services.verification.registry import VerificationRegistryService
from apps.api.app.services.verification.mapper import VerificationMapper

router = APIRouter(prefix="/verification", tags=["Verification"])
registry_service = VerificationRegistryService()
mapper_service = VerificationMapper()

@router.get("/sources")
def get_sources(db: Session = Depends(get_db)):
    return registry_service.list_sources(db)

@router.get("/source/{source_id}")
def get_source(source_id: str, db: Session = Depends(get_db)):
    source = registry_service.get_source_by_id(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Verification source not found")
    return source

@router.post("/map")
def map_claims(claims: list[str], db: Session = Depends(get_db)):
    return mapper_service.map_claims_to_sources(db, claims)
