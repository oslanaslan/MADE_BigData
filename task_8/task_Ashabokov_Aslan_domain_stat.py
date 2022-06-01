'''
Kafka with Spark Structured Streaming
'''
import argparse

from pyspark import SparkContext
from pyspark.sql.session import SparkSession
import pyspark.sql.functions as F


parser = argparse.ArgumentParser()
parser.add_argument("--kafka-brokers", required=True)
parser.add_argument("--topic-name", required=True)
parser.add_argument("--starting-offsets", default='latest')
group = parser.add_mutually_exclusive_group()
group.add_argument("--processing-time", default='0 seconds')
group.add_argument("--once", action='store_true')
args = parser.parse_args()

if args.once:
    args.processing_time = None
else:
    args.once = None

sc = SparkContext()
spark = SparkSession(sc)
spark.conf.set("spark.sql.shuffle.partitions", 50)

input_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", args.kafka_brokers)
    .option("subscribe", args.topic_name)
    .option("startingOffsets", args.starting_offsets)
    .load()
)
res_df = (
    input_df.selectExpr("cast(value as string)")
    .withColumn("domain", F.split(F.col("value"), "\t").getItem(2))
    .withColumn("UID", F.split(F.col("value"), "\t").getItem(1))
    .drop("value")
)
res_df.createOrReplaceTempView("page_views_tmp")
output = spark.sql("""
    select parse_url(domain, "HOST") as domain, count(uid) as view, approx_count_distinct(uid) as unique
    from page_views_tmp
    group by domain
    order by view desc
    limit 10
""")
query = (
    output
    .writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", "false")
    .trigger(once=args.once, processingTime=args.processing_time)
    .start()
)

query.awaitTermination()
