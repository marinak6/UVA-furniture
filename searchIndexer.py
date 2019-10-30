from kafka import KafkaConsumer
from kafka import errors as Errors
from elasticsearch import Elasticsearch


es = Elasticsearch(['es'])
connected = False
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
            print(item['name'])
