from pyspark import SparkContext
# while(True):
# Pull new messages from Kafka
# connected = False
# if(connected == False):
#     try:
#         print("try")
#         sc = SparkContext("spark://spark-master:7077", "PopularItems")
#         print("good")
#         connected = True
#     except:
#         print("bad")
#         connected = False
#         continue
# else:


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

# re-layout the data to ignore the user id
pages = pairs.map(lambda pairs: (pairs[0], [pairs[1]]))
# shuffle the data so that each key is only on one worker
count = pages.reduceByKey(lambda x, y: x+y)
# and then reduce all the values by adding them together
# bring the data back to the master node so we can print it out
# Step 2 output:
# output = count.collect()
# for page_id, count in output:
#     print((page_id, count))
# print("Step 2 items done")
# Mapping step 3
user_pairs = count.flatMap(lambda x: all_pairs(x[1]))
pairs_count = user_pairs.map(lambda x: (x, 1))
count_users = pairs_count.reduceByKey(lambda x, y: x+y)
filtered_results = count_users.filter(lambda x: x[1] > 2)
result = filtered_results.collect()
for item_id, count in result:
    print((item_id, count))
print("Step 3 items done")
sc.stop()
