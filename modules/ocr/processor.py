from ..real_driver import RealAIDriver
from core.database import ModuleStatus, StatusEnum
from sqlalchemy.orm import Session
import time
import base64

def process_ocr(div_secret_id: str, front_b64: str, back_b64: str, db: Session, driver=None):
    if driver is None:
        driver = RealAIDriver()
    # Provisioned Industrial OCR
    # Convert base64 to image, perform real scanning
    # For now, using modular mock driver
    
    result = driver.predict({"front": front_b64, "back": back_b64})
    
    status = db.query(ModuleStatus).filter(ModuleStatus.div_secret_id == div_secret_id, ModuleStatus.module_name == "OCR").first()
    if not status:
        status = ModuleStatus(div_secret_id=div_secret_id, module_name="OCR")
        db.add(status)
    
    status.status = StatusEnum.COMPLETED if result["status"] == "PASS" else StatusEnum.FAILED
    status.confidence_score = result["confidence"]
    if status.status == StatusEnum.FAILED:
        status.failure_reason = result.get("metadata", {}).get("reason", "OCR confidence threshold not met")
    db.commit()
    return result
