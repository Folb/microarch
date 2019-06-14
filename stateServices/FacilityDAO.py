from sqlalchemy import create_engine, Sequence, Column, Integer, DateTime, Boolean, String, Float
from sqlalchemy_utils import create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Facility(Base):
    __tablename__ = "facility"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)
    location_x = Column(Float, nullable=False)
    location_y = Column(Float, nullable=False)
    status = Column(String(256), nullable=False)
    open = Column(Boolean, nullable=False)
     

engine = create_engine("sqlite:///./dbs/facilities.db")
Base.metadata.create_all(engine)
