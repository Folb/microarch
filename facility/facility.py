import sys
import json
from collections import namedtuple
import os
from objects import Facility, Actuator, Sensor
from parser import Parser
import time
from kafka import KafkaProducer

#Kafka stuff
producer = KafkaProducer(bootstrap_servers='35.233.35.208:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

class SensorUpdate():
    def __init__(self, facility_id, sensor_id, new_value):
        self.facility_id = facility_id
        self.sensor_id = sensor_id
        self.new_value = new_value

def run_cycle(facility, cycle):
    for command in cycle: 
        update = SensorUpdate(facility.id, command.node_id, command.new_value)
        update = json.dumps(update, default=lambda o: o.__dict__)
        producer.send('test', update)

def get_cycle(simulation, start_point):
    cycle = []
    if start_point >= len(simulation):
        start_point = 0
    if simulation[start_point] == "|":
        start_point += 1
    while start_point < len(simulation) and simulation[start_point] != "|":
        cycle.append(simulation[start_point])
        start_point += 1

    return cycle, start_point

def run_simulation(facility):
    start_point = 0
    while True:
        cycle, start_point = get_cycle(facility.simulation, start_point)
        run_cycle(facility, cycle)
        time.sleep(2)

def parse_infile(infile):
    json_facility = None
    with open(infile) as f:
        json_facility = json.load(f)

    json_facility = json.loads(json.dumps(json_facility), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    return Parser.parse_facility(json_facility)

def main():
    infile = os.path.abspath(sys.argv[1])
    facility = parse_infile(infile)
    run_simulation(facility) 

if __name__ == '__main__':
    main()
