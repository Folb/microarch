from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from objects import *
import os
import ..stateServices

engine = create_engine('sqlite:///../stateServices/dbs/sensors.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

for facility in facilities:
    for sensor in facility['sensors']:
        

