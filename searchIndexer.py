from kafka import KafkaConsumer
from kafka import errors as Errors
from elasticsearch import Elasticsearch
import urllib.request
import urllib.parse
import json


es = Elasticsearch(['es'])
connected = False

# Index fixtures
req = urllib.request.Request(
    'http://microservices:8000/api/v1/get_items')

resp_json = urllib.request.urlopen(req).read().decode('utf-8')
resp = json.loads(resp_json)
listings = resp["Res"]
for item in listings:
    es.index(index='listing_index', doc_type='listing',
             id=item['id'], body=item)
    es.indices.refresh(index="listing_index")

while(True):
    # Pull new messages from Kafka
    if(connected == False):
        try:
            consumer = KafkaConsumer(
                'new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
            connected = True
        except Errors.NoBrokersAvailable:
            connected = False
            continue
    else:
        for message in consumer:
            item = json.loads((message.value).decode('utf-8'))
            # Index message in ES
            es.index(index='listing_index', doc_type='listing',
                     id=item['id'], body=item)
            es.indices.refresh(index="listing_index")
