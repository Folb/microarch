import sys
import json
from collections import namedtuple
import os
from objects import Facility, Actuator, Sensor
from parser import Parser
import time
import datetime
from kafka import KafkaProducer, KafkaConsumer

#Kafka stuff
bootstrap_servers = open('../bootstrapservers', 'r')
bootstrap_servers = bootstrap_servers.read().rstrip()

producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

class SensorUpdate():
    def __init__(self, facility_id, sensor_id, new_value):
        self.facility_id = facility_id
        self.sensor_id = sensor_id
        self.new_value = new_value

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

def post_message(message, topic):
    try:
        producer.send(topic, message)
    except:
        print("No broker for " + topic + " found")

def run_cycle(facility, cycle):
    for command in cycle: 
        update = SensorUpdate(facility.id, command.node_id, command.new_value)
        ts = datetime.datetime.now().timestamp()
        update.set_timestamp(ts)
        update = json.dumps(update, default=lambda o: o.__dict__)
        post_message(update, 'sensor_data')

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

update_consumer = KafkaConsumer('actuator_command', bootstrap_servers=bootstrap_servers)

def parse_message_to_dict(msg):
    msg = msg.value.decode('utf-8').replace("\\", "")
    msg = msg[1:-1]
    return json.loads(msg)

class ActuatorUpdate():
    def __init__(self, facility_id):
        self.facility_id = update['facility_id']
        self.actuator_id = update['actuator_id']
        self.new_status = update['new_status']

def update_actuator(facility, update):
    update = ActuatorUpdate(update)
    if facility.id != update.facility_id:
        return False

    for actuator in facility.actuators:
        if actuator.id == update.actuator_id:
            actuator.status = update.new_status
            return True
    return False

def poll_update_consumer(facility):
    msgs = update_consumer.poll(timeout_ms=200)
    for msg in msgs:
        update = parse_message_to_dict(msg)
        complete = update_actuator(facility, update)
        if complete:
            post_message(update, 'actuator_change')

def run_simulation(facility):
    start_point = 0
    while True:
        poll_update_consumer(facility)
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
