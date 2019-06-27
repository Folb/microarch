from sqlalchemy import create_engine, Sequence, Column, Integer, DateTime, Boolean, String
from sqlalchemy.orm import sessionmaker 
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
import json
import datetime

bootstrap_servers = open('../bootstrapservers', 'r')
bootstrap_servers = bootstrap_servers.read().rstrip()

#TODO consume update actuator requests from front-end
fe_consumer = KafkaConsumer('actuator_update', group_id='update_service', bootstrap_servers=bootstrap_servers)
#fe_consumer.assign([TopicPartition('actuator_update', 0)])

#TODO store requests in db 
Base = declarative_base()
class UpdateCommand(Base):
    __tablename__ = "update_commands"
    id = Column(Integer, Sequence("ucIdSeq"), primary_key=True)
    facility_id = Column(Integer, nullable=False)
    actuator_id = Column(Integer, nullable=False)
    complete = Column(Boolean, nullable=False)
    user = Column(String(100), nullable=False)
    new_status = Column(Boolean, nullable=False)
    timestamp_command = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    timestamp_complete = Column(DateTime, nullable=True)

    def __init__(self, facility_id, actuator_id, user, new_status):
        self.facility_id = facility_id
        self.actuator_id = actuator_id
        self.complete = False
        self.user = user
        self.new_status = new_status
        self.timestamp_command = datetime.datetime.now()
        self.timestamp_complete = None

db_url = 'sqlite:///./dbs/updateCommands.db'
engine = create_engine(db_url)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
if not database_exists(db_url): 
    Base.metadata.create_all(engine)

def store_actuator_update(actuator_update):
    session = DBSession()
    session.add(parse_actuator_update(actuator_update))
    session.commit()
    session.close()

def parse_actuator_update(msg):
    f_id = msg['facility_id']
    a_id = msg['actuator_id']
    user = msg['user']
    new_status = msg['new_status']
    return UpdateCommand(f_id, a_id, user, new_status)

#TODO produce updates to actuators
actuator_update_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, 
        value_serializer=lambda v: json.dumps(v).encode('utf-8')) 

def post_message(message, topic):
    try:
        actuator_update_producer.send(topic, message)
    except:
        print("No broker for " + topic + " found")

#TODO receive change status and notify front-end
actuator_change_consumer = KafkaConsumer('actuator_change', group_id='update_service', bootstrap_servers=bootstrap_servers)
#actuator_change_consumer.assign([TopicPartition('actuator_update_complete', 0)])

def set_update_to_complete(actuator_update):
    session = DBSession()
    update = session.query(UpdateCommand).filter_by(id = actuator_update.id)
    update.complete = True
    update.timestamp_complete = datetime.datetime.now()
    session.commit()
    session.close()

#TODO Service Loop
def parse_message_to_dict(msg):
    msg = msg.value.decode('utf-8').replace('\\', '')
    msg = msg[1:-1]
    return json.loads(msg)

while True:
    update_message = parse_message_to_dict(next(fe_consumer))
    print(update_message)
    store_actuator_update(update_message)
    post_message(update_message, 'actuator_command')
    facility_message = parse_message_to_dict(next(actuator_change_consumer))
    print(facility_message)
    set_update_to_complete(facility_message)
