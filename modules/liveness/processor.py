from ..real_driver import RealAIDriver
from core.database import ModuleStatus, StatusEnum
from sqlalchemy.orm import Session
import time

def process_liveness(div_secret_id: str, selfie_b64: str, db: Session, driver=None):
    if driver is None:
        driver = RealAIDriver()
    # Industrial Liveness
    # Run real spoofing detection ML model
    
    result = driver.predict({"selfie": selfie_b64})
    
    status = db.query(ModuleStatus).filter(ModuleStatus.div_secret_id == div_secret_id, ModuleStatus.module_name == "LIVENESS").first()
    if not status:
        status = ModuleStatus(div_secret_id=div_secret_id, module_name="LIVENESS")
        db.add(status)
    
    status.status = StatusEnum.COMPLETED if result["status"] == "PASS" else StatusEnum.FAILED
    status.confidence_score = result["confidence"]
    if status.status == StatusEnum.FAILED:
        status.failure_reason = "Liveness check failed: possible spoofing detected"
    db.commit()
    return result
