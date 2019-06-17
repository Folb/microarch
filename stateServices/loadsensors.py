import sys
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import namedtuple
from sensorDAO import SensorState
sys.path.insert(0, os.path.abspath('../facility'))
from parser import Parser


engine = create_engine("sqlite:///./dbs/sensors.db")

facility_directory = os.path.abspath('../facility/facilities/')
facilities = []
for filename in os.listdir(facility_directory):
    filename = facility_directory + "/" + filename
    if filename.endswith('.json'):
        with open(filename) as f:
            json_facility = json.load(f)

        json_facility = json.loads(json.dumps(json_facility), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        fac = Parser.parse_facility(json_facility)
        facilities.append(fac)

DBSession = sessionmaker(bind=engine)
session = DBSession()

sensors = []
for facility in facilities:
    for sensor in facility.sensors:
        ss = SensorState(sensor.id, facility.id, sensor.type, sensor.value, sensor.network_status)
        session.add(ss)
        sensors.append(ss)

session.add_all(sensors)
session.commit()

session.close()
