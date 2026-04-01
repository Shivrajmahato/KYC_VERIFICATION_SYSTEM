from pydantic import BaseModel
from typing import Optional

class SessionCreateRequest(BaseModel):
    tenant_id: str
    client_id: str
    user_id: str

class DocumentUploadRequest(BaseModel):
    document_front_image: str
    document_back_image: str

class LivenessUploadRequest(BaseModel):
    selfie_image: str
