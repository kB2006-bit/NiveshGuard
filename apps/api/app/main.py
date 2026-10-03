from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from .core.security import create_session, get_session
from .schemas.session import SessionCreate, SessionResponse
from .services.intake import intake_service
from .services.ai.extraction import extraction_service
from .services.ai.manipulation import manipulation_engine
from .api import incidents, verification
from .core.database import engine, Base
from .services.verification.registry import VerificationRegistryService

app = FastAPI(title="NiveshGuard API")

# Create database tables on startup for testing
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # Seed the verification registry
    registry = VerificationRegistryService()
    from .core.database import SessionLocal
    db = SessionLocal()
    try:
        registry.seed_registry(db)
    finally:
        db.close()

app.include_router(incidents.router, prefix="/api/v1")
app.include_router(verification.router, prefix="/api/v1")

# Temporary store for results (since Phase 1 persistence is minimal)
results_cache = {}

@app.get("/")
async def root():
    return {"message": "NiveshGuard API is running"}

@app.post("/api/v1/session", response_model=SessionResponse)
async def start_session(req: SessionCreate):
    session_id = create_session()
    return {
        "session_id": session_id,
        "language": req.language,
        "mode": req.mode
    }

@app.post("/api/v1/analyze/upload")
async def upload_content(
    file: UploadFile = File(...),
    input_type: str = Form(...),
    session_id: str = Form(...)
):
    if not get_session(session_id):
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    try:
        intake_result = intake_service.process_upload(file, input_type)
        text = intake_result["text"]

        extraction_result = await extraction_service.extract_claims_and_entities(text)
        manipulation_result = await manipulation_engine.detect_patterns(
            text, 
            extraction_result.get("claims", [])
        )

        response_data = {
            "session_id": session_id,
            "extracted_text": text,
            "analysis": {
                "claims": extraction_result.get("claims", []),
                "entities": extraction_result.get("entities", []),
                "manipulation_signals": manipulation_result.get("signals", []),
                "metadata": intake_result["metadata"]
            }
        }
        
        # Cache the result for the frontend to fetch
        results_cache[session_id] = response_data
        
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/api/v1/analyze/result/{session_id}")
async def get_analysis_result(session_id: str):
    result = results_cache.get(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    return result

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}
