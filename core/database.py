from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid
import enum

DATABASE_URL = "sqlite:///./kyc_sessions.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class VerificationSession(Base):
    __tablename__ = "verification_sessions"

    div_secret_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False)
    client_id = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=False)
    request_id = Column(String(64), nullable=False, unique=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    module_statuses = relationship("ModuleStatus", back_populates="session")

class ModuleStatus(Base):
    __tablename__ = "module_status"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    div_secret_id = Column(String(64), ForeignKey("verification_sessions.div_secret_id"))
    module_name = Column(String(32), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    confidence_score = Column(Float, nullable=True)
    failure_reason = Column(String(255), nullable=True)  # New transparency field
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("VerificationSession", back_populates="module_statuses")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
