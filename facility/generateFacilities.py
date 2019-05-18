import sys
import random
import json 
import os, shutil
import math

from objects import Facility, Actuator, Sensor

base_names = [
        'Knappe',
        'Årdal',
        'Tynseth',
        'Fløyfjell',
        'Brevik',
        'Sputtum']

numbered_names = {}
for name in base_names:
    numbered_names[name] = 1

facility_type = [
        'tunell',
        'bro',
        'kryss']

sensor_types = [
        'temperature',
        'camera', 
        'nox',
        'co',
        'noise']

actuator_types = [
        'barrier',
        'lights',
        'sound']

def gen_random_coordinate():
    x = 60.390428
    y = 5.328410
    theta = 2 * math.pi * random.random()
    s = 3 * random.random()
    coordinate = (x + s * math.cos(theta), y + s * math.sin(theta))
    return str(coordinate)

gen_size = int(sys.argv[1])

#Delete old facility files
folder = os.path.abspath("facilities")
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    if "init.txt" in file_path:
        continue
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

#Generate new facilities
s_id = 0
a_id = 0
for i in range(0, gen_size):
    base_name = random.choice(base_names)
    name = base_name + str(numbered_names[base_name])
    numbered_names[base_name] += 1
    
    t = random.choice(facility_type)

    location = gen_random_coordinate()

    nmb_sensors = random.randint(5, 20)
    sensors = []
    for j in range(s_id, s_id + nmb_sensors):
        s = Sensor()
        s.set_id(s_id)
        s.set_type(random.choice(sensor_types))
        s.set_value(10)
        s.set_network_status('online')
        sensors.append(s)
        s_id += 1

    nmb_actuators = random.randint(2, 10)
    actuators = []
    for j in range(a_id, a_id + nmb_actuators):
        a = Actuator()
        a.set_id(a_id)
        a.set_type(random.choice(actuator_types))
        a.set_status('not active')
        a.set_network_status('online')
        actuators.append(a)
        a_id += 1

    fac = Facility()
    fac.set_name(name)
    fac.set_type(t)
    fac.set_location(location)
    fac.set_status('normal')
    fac.set_open(True)
    fac.set_sensors(sensors)
    fac.set_actuators(actuators)

    with open('facilities/' + name + '.json', 'w') as outfile:
        json.dump(fac, outfile, default=lambda o: o.__dict__)

print('Done')
