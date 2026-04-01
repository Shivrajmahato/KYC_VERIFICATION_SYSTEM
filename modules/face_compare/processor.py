from ..real_driver import RealAIDriver
from core.database import ModuleStatus, StatusEnum
from sqlalchemy.orm import Session
import time

def process_face_compare(div_secret_id: str, front_b64: str, selfie_b64: str, db: Session, driver=None):
    if driver is None:
        driver = RealAIDriver()
    # Industrial Face Matching
    # Prediction based on threshold logic
    
    result = driver.predict({"pair": [front_b64, selfie_b64]})
    
    status = db.query(ModuleStatus).filter(ModuleStatus.div_secret_id == div_secret_id, ModuleStatus.module_name == "FACE_COMPARE").first()
    if not status:
        status = ModuleStatus(div_secret_id=div_secret_id, module_name="FACE_COMPARE")
        db.add(status)
    
    status.status = StatusEnum.COMPLETED if result["status"] == "PASS" else StatusEnum.FAILED
    status.confidence_score = result["confidence"]
    if status.status == StatusEnum.FAILED:
        status.failure_reason = "Face similarity below threshold"
    db.commit()
    return result
