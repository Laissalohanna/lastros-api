from sqlalchemy import Column, BigInteger, String, JSON, DateTime
from datetime import datetime
from db.base import Base


class ProjectConfig(Base):
    __tablename__ = "ProjectConfig"
    

    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    ProjectUid = Column(String, nullable=False)
    Alias = Column(String, nullable=False)
    Config = Column(JSON, nullable=False)
    CreatedDate = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    UpdatedDate = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    DeletedAt = Column(DateTime(timezone=True), nullable=True)