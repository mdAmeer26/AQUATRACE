"""
Database Models
SQLAlchemy models for AquaTrace data storage
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from geoalchemy2 import Geometry

Base = declarative_base()


class MicroplasticObservation(Base):
    """
    Individual microplastic concentration observation
    """
    __tablename__ = 'microplastic_observations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    concentration = Column(Float, nullable=False)
    confidence = Column(Float)
    source = Column(String(50))  # 'CYGNSS', 'Sentinel', 'ML_Model'
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """
    Microplastic concentration alerts
    """
    __tablename__ = 'alerts'
    
    id = Column(String(100), primary_key=True)
    severity = Column(String(20), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    concentration = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    region = Column(String(100))
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProcessingRun(Base):
    """
    Track data processing runs
    """
    __tablename__ = 'processing_runs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_date = Column(DateTime, nullable=False)
    data_source = Column(String(50))
    observations_processed = Column(Integer)
    alerts_generated = Column(Integer)
    status = Column(String(20))  # 'completed', 'failed', 'running'
    error_message = Column(String(500))
    metadata = Column(JSON)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
