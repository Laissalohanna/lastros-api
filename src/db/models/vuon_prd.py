import uuid
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base


class BaseFiles(Base):
    __tablename__ = "BaseFiles"

    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    ExternalId = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    Code = Column(BigInteger, nullable=False)
    FileName = Column(Text, nullable=False)
    FileExtension = Column(Text, nullable=False)
    Company = Column(Text, nullable=True)

    ProcessingDate = Column(DateTime(timezone=True), nullable=True)
    CreatedDate = Column(DateTime(timezone=True), nullable=True)
    UpdatedDate = Column(DateTime(timezone=True), nullable=True)
    DeletedAt = Column(DateTime(timezone=True), nullable=True)

    FileSubType = Column(Integer, nullable=False, default=0)
    FileSubTypeId = Column(BigInteger, nullable=False, default=0)
    ProjectUid = Column(String(13), nullable=True)
    TransactionUid = Column(UUID(as_uuid=True), nullable=True, default=uuid.uuid4)
