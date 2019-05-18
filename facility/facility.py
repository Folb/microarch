import sys
import json
from collections import namedtuple
import os
from objects import Facility, Actuator, Sensor
from parser import Parser
import time

def run_simulation(facility):
    while True:
        sleep(5)

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
