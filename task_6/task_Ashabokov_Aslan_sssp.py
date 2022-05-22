'''
Twitter bfs count
'''
from math import inf
from collections import deque, defaultdict

from pyspark import SparkContext
from pyspark.sql.session import SparkSession
import pyspark.sql.functions as F


TWITTER_SRC = "hdfs:///data/twitter/twitter.txt"
# TWITTER_SRC = "/data/twitter/twitter_sample.txt"
# TWITTER_SRC = "/data/twitter/twitter_sample_small.txt"


def bfs_func(target):
    '''BFS'''
    bfs_res_dct[target] = 0
    deq = deque()
    deq.append(target)
    used_dct[target] = True

    while len(deq) != 0:
        node_v = deq.popleft()

        for node_u in graph_dct[node_v]:
            if not used_dct[node_u]:
                used_dct[node_u] = True
                deq.append(node_u)
                bfs_res_dct[node_u] = bfs_res_dct[node_v] + 1


sc = SparkContext()
spark = SparkSession(sc)
edges_df = spark.read.text(TWITTER_SRC)

edges_list = (edges_df.withColumn("from", F.split(F.col("value"), "\t").getItem(1))
                      .withColumn("to", F.split(F.col("value"), "\t").getItem(0))
                      .drop("value"))
graph_df = (edges_list.groupBy("from").agg(F.collect_list("to").alias("to_nodes")))
unique_nodes = (edges_list
                .select(F.col("from").alias("node"))
                .union(edges_list.select(F.col("to").alias("node")))
                .distinct())


unique_nodes_list = list(map(lambda row: row["node"], unique_nodes.collect()))
graph_dct = defaultdict(list)
bfs_res_dct = defaultdict(int)
used_dct = defaultdict(bool)

for row in graph_df.collect():
    graph_dct[row["from"]].extend(row["to_nodes"])

for node in unique_nodes_list:
    bfs_res_dct[node] = inf
    used_dct[node] = False

bfs_func("12")
res = bfs_res_dct["34"]
spark.stop()
print(res)
