import logging
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from core.database import get_db, Base, engine, VerificationSession, ModuleStatus, StatusEnum
from core.schemas import SessionCreateRequest, DocumentUploadRequest, LivenessUploadRequest
from core.security import generate_div_secret_id

from modules.ocr.processor import process_ocr
from modules.face_compare.processor import process_face_compare
from modules.liveness.processor import process_liveness
import os
import time
import random

# Configure Industrial Logging
logger = logging.getLogger("KYC_GATEWAY")
logger.setLevel(logging.INFO)

# File Handler (Debug)
fh = logging.FileHandler("debug.log", mode='a')
fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(fh)

# Audit Logger (Security Tracing)
audit_logger = logging.getLogger("KYC_AUDIT")
audit_logger.setLevel(logging.INFO)
ah = logging.FileHandler("audit.log", mode='a')
ah.setFormatter(logging.Formatter('%(asctime)s [AUDIT] %(message)s'))
audit_logger.addHandler(ah)

# Stream Handler (Terminal)
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter('%(levelname)s:     %(message)s'))
logger.addHandler(sh)

logger.info("KYC Gateway: System logging initialized and ready.")
audit_logger.info("Security Audit subsystem online.")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="KYC DIV_SECRET_ID Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_and_trigger_face_compare(div_secret_id: str):
    from core.database import SessionLocal
    db = SessionLocal()
    try:
        ocr_mod = db.query(ModuleStatus).filter(ModuleStatus.div_secret_id == div_secret_id, ModuleStatus.module_name == "OCR").first()
        live_mod = db.query(ModuleStatus).filter(ModuleStatus.div_secret_id == div_secret_id, ModuleStatus.module_name == "LIVENESS").first()
        session = db.query(VerificationSession).filter(VerificationSession.div_secret_id == div_secret_id).first()
        
        if not ocr_mod or not live_mod:
            return

        # Terminal state logic: Check if both prerequisites are FINISHED (whether PASS or FAIL)
        if ocr_mod.status in [StatusEnum.COMPLETED, StatusEnum.FAILED] and \
           live_mod.status in [StatusEnum.COMPLETED, StatusEnum.FAILED]:
            
            # If BOTH must pass to trigger Face Compare
            if ocr_mod.status == StatusEnum.COMPLETED and live_mod.status == StatusEnum.COMPLETED:
                logger.info(f"Prerequisites PASSED. Triggering Face Compare for {div_secret_id}")
                process_face_compare(div_secret_id, "s3_reference_front", "s3_reference_selfie", db)
                
                # Final Final check
                fc_mod = db.query(ModuleStatus).filter(ModuleStatus.div_secret_id == div_secret_id, ModuleStatus.module_name == "FACE_COMPARE").first()
                if fc_mod and fc_mod.status == StatusEnum.COMPLETED:
                    session.confidence_score = fc_mod.confidence_score
                    session.status = StatusEnum.COMPLETED if (session.confidence_score or 0) > 0.8 else StatusEnum.FAILED
                    audit_logger.info(f"Final Decision for User {session.user_id}: {session.status} (Score: {session.confidence_score})")
                else:
                    session.status = StatusEnum.FAILED
                    audit_logger.error(f"Final Decision for User {session.user_id}: FAILED (Face Compare logic error)")
            else:
                # One or both failed OCR/Liveness
                logger.warning(f"Prerequisites FAILED for {div_secret_id}. Session REJECTED.")
                session.status = StatusEnum.FAILED
                audit_logger.warning(f"Final Decision for User {session.user_id}: REJECTED (Prerequisite Failure)")
            
            db.commit()
    finally:
        db.close()

import base64
from core.storage import storage_manager

def run_ocr_task(div_secret_id: str, req: DocumentUploadRequest):
    from core.database import SessionLocal
    db = SessionLocal()
    try:
        logger.info(f"Task OCR: Starting for session {div_secret_id}")
        # Save to Storage (MinIO or Local)
        try:
            front_b64 = req.document_front_image.split(",")[-1]
            back_b64 = req.document_back_image.split(",")[-1]
            
            # Pad if necessary for robustness
            missing_padding = len(front_b64) % 4
            if missing_padding: front_b64 += '=' * (4 - missing_padding)
            missing_padding = len(back_b64) % 4
            if missing_padding: back_b64 += '=' * (4 - missing_padding)

            front_bytes = base64.b64decode(front_b64)
            back_bytes = base64.b64decode(back_b64)
            
            if front_bytes: 
                res = storage_manager.upload_file(front_bytes, f"{div_secret_id}/front.jpg")
                logger.info(f"Task OCR: Front upload -> {res}")
            if back_bytes: 
                res = storage_manager.upload_file(back_bytes, f"{div_secret_id}/back.jpg")
                logger.info(f"Task OCR: Back upload -> {res}")
        except Exception as e:
            logger.error(f"Task OCR Storage Error: {e}")
            
        process_ocr(div_secret_id, req.document_front_image, req.document_back_image, db)
        check_and_trigger_face_compare(div_secret_id)
    except Exception as e:
        logger.critical(f"Task OCR Critical Failure: {e}")
    finally:
        db.close()

def run_liveness_task(div_secret_id: str, req: LivenessUploadRequest):
    from core.database import SessionLocal
    db = SessionLocal()
    try:
        logger.info(f"Task Liveness: Starting for session {div_secret_id}")
        # Save to Storage
        try:
            selfie_b64 = req.selfie_image.split(",")[-1]
            missing_padding = len(selfie_b64) % 4
            if missing_padding: selfie_b64 += '=' * (4 - missing_padding)
            
            selfie_bytes = base64.b64decode(selfie_b64)
            if selfie_bytes: 
                res = storage_manager.upload_file(selfie_bytes, f"{div_secret_id}/selfie.jpg")
                logger.info(f"Task Liveness: Selfie upload -> {res}")
        except Exception as e:
            logger.error(f"Task Liveness Storage Error: {e}")
            
        process_liveness(div_secret_id, req.selfie_image, db)
        check_and_trigger_face_compare(div_secret_id)
    except Exception as e:
        logger.critical(f"Task Liveness Critical Failure: {e}")
    finally:
        db.close()

@app.post("/gateway/session/start")
async def start_session(req: SessionCreateRequest, db: Session = Depends(get_db)):
    logger.info(f"API: Start Session requested for user {req.user_id}")
    audit_logger.info(f"Session started for User: {req.user_id} (Tenant: {req.tenant_id}, Client: {req.client_id})")
    security_data = generate_div_secret_id(req.tenant_id, req.client_id)
    div_secret_id = security_data["div_secret_id"]
    
    new_session = VerificationSession(
        div_secret_id=div_secret_id,
        tenant_id=req.tenant_id,
        client_id=req.client_id,
        user_id=req.user_id,
        request_id=security_data["request_id"],
        status=StatusEnum.IN_PROGRESS
    )
    db.add(new_session)
    db.commit()
    
    return {
        "div_secret_id": div_secret_id,
        "status": "SESSION_STARTED"
    }

@app.post("/gateway/session/{div_secret_id}/document")
async def upload_document(div_secret_id: str, req: DocumentUploadRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.info(f"API: Document upload requested for session {div_secret_id}")
    session = db.query(VerificationSession).filter(VerificationSession.div_secret_id == div_secret_id).first()
    if not session:
        logger.warning(f"API: Session {div_secret_id} not found for document upload")
        audit_logger.warning(f"Unauthorized/Invalid access attempt to document upload for session {div_secret_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    audit_logger.info(f"Documents uploaded for User {session.user_id} (Session: {div_secret_id})")
    background_tasks.add_task(run_ocr_task, div_secret_id, req)
    return {"message": "Document uploaded and OCR processing started"}

@app.post("/gateway/session/{div_secret_id}/liveness")
async def upload_liveness(div_secret_id: str, req: LivenessUploadRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.info(f"API: Liveness upload requested for session {div_secret_id}")
    session = db.query(VerificationSession).filter(VerificationSession.div_secret_id == div_secret_id).first()
    if not session:
        logger.warning(f"API: Session {div_secret_id} not found for liveness upload")
        audit_logger.warning(f"Unauthorized/Invalid liveness attempt for session {div_secret_id}")
        raise HTTPException(status_code=404, detail="Session not found")
        
    audit_logger.info(f"Liveness image uploaded for User {session.user_id} (Session: {div_secret_id})")
    background_tasks.add_task(run_liveness_task, div_secret_id, req)
    return {"message": "Selfie uploaded and Liveness processing started"}

@app.get("/gateway/status/{div_secret_id}")
async def get_status(div_secret_id: str, db: Session = Depends(get_db)):
    session = db.query(VerificationSession).filter(VerificationSession.div_secret_id == div_secret_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    modules = db.query(ModuleStatus).filter(ModuleStatus.div_secret_id == div_secret_id).all()
    
    return {
        "div_secret_id": session.div_secret_id,
        "overall_status": session.status,
        "final_confidence": session.confidence_score,
        "modules": [
            {
                "module": mod.module_name, 
                "status": mod.status, 
                "confidence_score": mod.confidence_score,
                "failure_reason": mod.failure_reason
            } for mod in modules
        ]
    }
