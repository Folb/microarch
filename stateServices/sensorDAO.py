from sqlalchemy import create_engine, Sequence, ForeignKey, Column, Integer, DateTime, Boolean, String, Float
from sqlalchemy_utils import create_database
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SensorState(Base):
    __tablename__ = "sensor_state"
    id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, nullable=False)
    type = Column(String(30), nullable=False)
    value = Column(Float, nullable=False)
    network_status = Column(String(10), nullable=False)

class SensorHistoric(Base):
    __tablename__ = "historic_sensor_data"
    id = Column(Integer, Sequence("sIdSeq"), primary_key=True)
    s_id = Column(Integer, ForeignKey("sensor_state.id"), nullable=False )
    value = Column(Float, nullable=False)
    network_status = Column(String(10), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sensor_state = relationship(SensorState)

engine = create_engine("sqlite:///./dbs/sensors.db")
Base.metadata.create_all(engine)
