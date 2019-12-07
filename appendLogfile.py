from kafka import KafkaConsumer
from kafka import errors as Errors
from elasticsearch import Elasticsearch
import urllib.request
import urllib.parse
import json
import time
connected = False

while(True):
    # Pull new messages from Kafka
    time.sleep(60)
    if(connected == False):
        try:
            consumer2 = KafkaConsumer(
                'page-view', group_id='page-view-process', bootstrap_servers=['kafka:9092'])
            connected = True
        except Errors.NoBrokersAvailable:
            connected = False
            continue
    else:
        for message in consumer2:
            view = json.loads((message.value).decode('utf-8'))

            f = open("./data/logfile.txt", "a")
            f.write(str(view["user_id"])+","+str(view["item_id"])+"\n")
