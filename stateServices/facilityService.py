from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(bootstrap_servers='35.233.35.208:9092')
consumer.assign([TopicPartition('test', 0)])
while True:
    msg = next(consumer)
    print(msg.value)

