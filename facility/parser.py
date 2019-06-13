from objects import *
import json

class Parser():
    def parse_facility(json_f):
        f = Facility()
        f.set_id(json_f.id)
        f.set_name(json_f.name)
        f.set_type(json_f.type)
        f.set_location(json_f.location)
        f.set_status(json_f.status)
        f.set_open(json_f.open)
        f.set_sensors(Parser.parse_sensors(json_f.sensors))
        f.set_actuators(Parser.parse_actuators(json_f.actuators))
        f.set_simulation(Parser.parse_simulation(json_f.simulation))
        return f

    def parse_sensors(sensors):
        ret = []
        for sensor in sensors:
            s = Sensor()
            s.set_id(sensor.id)
            s.set_type(sensor.type)
            s.set_value(sensor.value)
            s.set_network_status(sensor.network_status)
            ret.append(s)

        return ret

    def parse_actuators(actuators):
        ret = [] 
        for actuator in actuators:
            a = Actuator()
            a.set_id(actuator.id)
            a.set_type(actuator.type)
            a.set_status(actuator.status)
            a.set_network_status(actuator.network_status)
            ret.append(a)

        return ret

    def parse_simulation(simulation):
        ret = []
        for command in simulation:
            if command == "|":
                ret.append(command)
                continue
            c = Command(command.node_type, command.node_id)
            c.set_new_value(command.new_value)
            ret.append(c)

        return ret
