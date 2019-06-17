from sqlalchemy import create_engine, Sequence, ForeignKey, Column, Integer, DateTime, Boolean, String, Float
from sqlalchemy_utils import create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SensorState(Base):
    __tablename__ = "sensor_state"
    id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, nullable=False)
    type = Column(String(30), nullable=False)
    value = Column(Float, nullable=False)
    network_status = Column(String(10), nullable=False)

    def __init__(self, s_id, facility_id, s_type, value, network_status):
        self.id = s_id
        self.facility_id = facility_id
        self.type = s_type
        self.value = value
        self.network_status = network_status

class SensorHistoric(Base):
    __tablename__ = "historic_sensor_data"
    id = Column(Integer, Sequence("sIdSeq"), primary_key=True)
    s_id = Column(Integer, nullable=False )
    value = Column(Float, nullable=False)
    timestamp = Column(Float, nullable=False)

    def __init__(self, s_id, value, timestamp):
        self.s_id = s_id
        self.value = value
        self.timestamp = timestamp

engine = create_engine("sqlite:///./dbs/sensors.db")
Base.metadata.create_all(engine)
