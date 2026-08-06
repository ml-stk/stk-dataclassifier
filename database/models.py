from sqlalchemy import Column, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum

Base = declarative_base()

class TierEnum(str, enum.Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"

class FileMetadataModel(Base):
    __tablename__ = "file_metadata"

    file_id = Column(String, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    assigned_tier = Column(SQLEnum(TierEnum), default=TierEnum.INTERNAL, nullable=False)
    confidence_score = Column(Float, default=1.0)
    matched_rules = Column(Text, nullable=True)
    tagged_by = Column(String, default="System-Automated")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)