from sqlalchemy import create_engine, Sequence, Column, Integer, DateTime, Boolean, String
from sqlalchemy.orm import sessionmaker 
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
import json

bootstrap_servers = '35.233.35.208:9092'

#TODO consume update actuator requests from front-end
fe_consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
fe_consumer.assign([TopicPartition('actuator_update', 0)])

#TODO store requests in db 
Base = declarative_base()
class UpdateCommand(Base):
    __tablename__ = "update_commands"
    id = Column(Integer, Sequence(ucIdSeq), primary_key=True)
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

def set_update_to_complete(actuator_update):
    session = DBSession()
    update = session.query(UpdateCommand).filter_by(id = actuator_update.id)
    update.complete = True
    update.timestamp_complete = datetime.datetime.now()
    session.commit()
    session.close()

def store_actuator_update(actuator_update):
    session = DBSession()
    session.add(actuator_update)
    session.commit()
    session.close()

#TODO produce updates to zactuators
actuator_update_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, 
        value_serializer=lambda v: json.dumps(v).encode('utf-8')) 

def post_message(message, topic):
    try:
        actuator_update_producer.send(topic, message)
    except:
        print("No broker for " + topic + " found")

#TODO receive change status and notify front-end

def parse_message_to_dict(msg):
    msg = msg.value.decode('utf-8').replace('\\', '')
    msg = msg[1:-1]
    return json.loads(msg)

while True:
    msg = parse_message_to_dict(next(fe_consumer))
    #TODO transform and publish to facility_updates
