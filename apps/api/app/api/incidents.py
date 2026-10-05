from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.incident import Incident
from ..models.evidence import EvidencePack, EvidenceItem
from ..services.evidence import EvidenceService
import uuid
from datetime import datetime

router = APIRouter(prefix="/incidents", tags=["Incidents"])
evidence_service = EvidenceService()

@router.post("/")
def create_incident(user_id: str, user_notes: str = None, db: Session = Depends(get_db)):
    incident = Incident(
        incident_id=str(uuid.uuid4()),
        user_id=user_id,
        user_notes=user_notes,
        incident_date=datetime.utcnow()
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@router.post("/{incident_id}/evidence-pack")
def create_evidence_pack(incident_id: str, description: str = None, db: Session = Depends(get_db)):
    # Verify incident exists
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    pack = evidence_service.create_evidence_pack(db, incident_id, description)
    return pack

@router.post("/evidence-packs/{pack_id}/items")
def add_evidence_item(pack_id: str, file_name: str, file_path: str, file_type: str, metadata: str = None, db: Session = Depends(get_db)):
    pack = evidence_service.get_evidence_pack(db, pack_id)
    if not pack:
        raise HTTPException(status_code=404, detail="Evidence pack not found")

    item = evidence_service.add_evidence_item(db, pack_id, file_name, file_path, file_type, metadata)
    return item

@router.get("/{incident_id}/evidence")
def get_incident_evidence(incident_id: str, db: Session = Depends(get_db)):
    packs = evidence_service.get_packs_for_incident(db, incident_id)
    evidence_data = []
    for pack in packs:
        items = evidence_service.get_evidence_items(db, pack.pack_id)
        evidence_data.append({
            "pack_id": pack.pack_id,
            "description": pack.description,
            "created_at": pack.created_at,
            "items": items
        })
    return evidence_data

@router.get("/{incident_id}/summary")
def get_incident_summary(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    packs = evidence_service.get_packs_for_incident(db, incident_id)
    total_items = sum(len(evidence_service.get_evidence_items(db, pack.pack_id)) for pack in packs)
    
    return {
        "incident_id": incident.incident_id,
        "date": incident.incident_date,
        "summary": f"Incident reported with {len(packs)} evidence pack(s) containing {total_items} item(s).",
        "notes": incident.user_notes
    }
