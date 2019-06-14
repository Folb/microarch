from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from kafka import KafkaConsumer, TopicPartition
import json

bootstrap_servers = '35.233.35.208:9092'

consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
consumer.assign([TopicPartition('test', 0)])

while True:
    msg = next(consumer)
    msg = msg.value.decode("utf-8").replace("\\", "")
    msg = msg[1:-1]
    msg = json.loads(msg)
