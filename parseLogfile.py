
from elasticsearch import Elasticsearch

import json
import time
from collections import defaultdict
es = Elasticsearch(['es'])
es_connected = False

while not es_connected:
    if es.ping():
        es_connected = True
while(True):
    # Pull new messages from Kafka
    time.sleep(600)
    es.ping()
    with open("logfile.txt", 'r') as f:
        get_all = f.readlines()
    with open("logfile.txt", 'w') as f:
        for i, line in enumerate(get_all, 1):
            split_line = line.split(",")
            if split_line[-1][0] == "0":
                item_id = int(split_line[1])
                try:
                    es.update(index='listing_index', doc_type='listing',
                              id=item_id, body={'script': 'ctx._source.visits += 1'})
                except:
                    es.update(index='listing_index', doc_type='listing', id=item_id, body={
                        'script': 'ctx._source.visits = 1'})
                split_line[-1] = "1\n"
                f.writelines(",".join(split_line))
            else:
                f.writelines(",".join(split_line))
