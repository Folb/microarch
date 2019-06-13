class Facility():
    def __init__(self):
        pass

    def set_id(self, i):
        self.id = i

    def set_name(self, name):
        self.name = name

    def set_type(self, t):
        self.type = t

    def set_location(self, coordinate):
        self.location = coordinate
    
    def set_status(self, s):
        self.status = s

    def set_open(self, o):
        self.open = o

    def set_sensors(self, sensors):
        self.sensors = sensors

    def set_actuators(self, actuators):
        self.actuators = actuators

    def set_simulation(self, simulation):
        self.simulation = simulation

class Actuator():
    def __init__(self):
        pass

    def set_id(self, i):
        self.id = i

    def set_type(self, t):
        self.type = t

    def set_status(self, s):
        self.status = s

    def set_network_status(self, ns):
        self.network_status = ns

class Sensor():
    def __init__(self):
        pass
    
    def set_id(self, i):
        self.id = i

    def set_type(self, t):
        self.type = t

    def set_value(self, v):
        self.value = v

    def set_network_status(self, s):
        self.network_status = s

class Command():
    def __init__(self, node_type, node_id):
        self.node_type = node_type
        self.node_id = node_id

    def set_new_value(self, val):
        self.new_value = val


