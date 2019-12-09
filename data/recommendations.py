from pyspark import SparkContext
from collections import defaultdict
import urllib.request
import urllib.parse


def all_pairs(items):
    list_tuples = []
    for i in range(0, len(items)):
        for j in range(i+1, len(items)):
            if(i == j):
                continue
            first_item = items[i]
            second_item = items[j]
            list_tuples.append((first_item, second_item))
            list_tuples.append((second_item, first_item))

    return (list_tuples)


sc = SparkContext("spark://spark-master:7077", "PopularItems")
# each worker loads a piece of the data file
data = sc.textFile("/tmp/data/logfile.txt", 2)
# tell each worker to split each line of it's partition
distinct = data.distinct()
pairs = distinct.map(lambda line: line.split(","))
print("Step 1 Done")
# re-layout the data to ignore the user id
pages = pairs.map(lambda pairs: (int(pairs[0]), [int(pairs[1])]))
# shuffle the data so that each key is only on one worker
count = pages.reduceByKey(lambda x, y: x+y)
# and then reduce all the values by adding them together
# bring the data back to the master node so we can print it out
# Step 2 output:
print("Step 2 items done")
# Mapping step 3
user_pairs = count.flatMap(lambda x: all_pairs(x[1]))
pairs_count = user_pairs.map(lambda x: (x, 1))
count_users = pairs_count.reduceByKey(lambda x, y: x+y)
filtered_results = count_users.filter(lambda x: x[1] > 2)
result = filtered_results.collect()

recommendations = defaultdict(str)
for item_id, count in result:
    if recommendations[item_id[0]] == "":
        recommendations[item_id[0]] = str(item_id[1])
    else:
        recommendations[item_id[0]
                        ] = recommendations[item_id[0]]+","+str(item_id[1])
    print((item_id, count))


url = 'http://microservices:8000/api/v1/recommendation/create'
for rec in recommendations.keys():
    form_data = {"item_id": rec, "recommendations": recommendations[rec]}
    encode_form = urllib.parse.urlencode(form_data).encode('utf-8')
    new_request = urllib.request.Request(
        url, data=encode_form, method='POST')
    resp_json = urllib.request.urlopen(
        new_request).read().decode('utf-8')


print("Step 3 items done")
sc.stop()
