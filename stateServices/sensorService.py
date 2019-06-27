from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from kafka import KafkaConsumer, TopicPartition
import json
from sensorDAO import SensorState, SensorHistoric 

bootstrap_servers = open('../bootstrapservers')
bootstrap_servers = bootstrap_servers.read().rstrip()

consumer = KafkaConsumer('sensor_data', group_id='sensor_service', bootstrap_servers=bootstrap_servers)
#consumer.assign([TopicPartition('sensor_data', 0)])

Base = declarative_base()
engine = create_engine('sqlite:///./dbs/sensors.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

#TODO consume on get requests from front-end
#TODO produce list of entities

def parse_message_to_dict(msg):
    msg = msg.value.decode("utf-8").replace("\\", "")
    msg = msg[1:-1]
    return json.loads(msg)
    
class SensorUpdate(object):
    def update(self, session, msg):
        state = session.query(SensorState).filter_by(id = msg['sensor_id']).update({SensorState.value: msg['new_value']})

while True:
    session = DBSession()
    try:
        msg = parse_message_to_dict(next(consumer))
        print(msg)
        sh = SensorHistoric(msg['sensor_id'], msg['new_value'], msg['timestamp'])
    except:
        print("simons wrong doing")
    try:
        SensorUpdate().update(session, msg)
        session.add(sh)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
