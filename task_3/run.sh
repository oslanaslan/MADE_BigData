#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
HDFS_INPUT_DIR=${1}
HDFS_OUTPUT_DIR=${2}
JOB_NAME=${3}
NUM_REDUCERS=8
OUT_COUNT=20

hdfs dfs -rm -r -skipTrash ${HDFS_OUTPUT_DIR}* > /dev/null

# Wordcount
( yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.job.name=${JOB_NAME}_1 \
	-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
	-D stream.num.map.output.key.fields=2 \
	-D stream.num.reduce.output.key.fields=2 \
	-D mapreduce.partition.keypartitioner.options=-k1,1 \
	-D mapreduce.partition.keycomparator.options="-k1,1 -k2,2" \
        -files phase_1_mapper.py,phase_1_reducer.py \
	-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
	-numReduceTasks 2 \
        -mapper 'python3 phase_1_mapper.py' \
        -reducer 'python3 phase_1_reducer.py' \
	-combiner 'python3 phase_1_reducer.py' \
        -input $HDFS_INPUT_DIR \
	-output ${HDFS_OUTPUT_DIR}_tmp > /dev/null &&

# Global sorting as we use only 1 reducer
yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.job.name=${JOB_NAME}_2 \
	-D stream.num.map.output.key.fields=3 \
        -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
        -D mapred.text.key.comparator.options="-k1,1nr -k3,3nr" \
	-files phase_2_mapper.py,phase_2_reducer.py \
        -numReduceTasks 1 \
        -mapper 'python3 phase_2_mapper.py' \
        -reducer 'python3 phase_2_reducer.py' \
        -input ${HDFS_OUTPUT_DIR}_tmp \
        -output ${HDFS_OUTPUT_DIR} \
	> /dev/null
) || echo "Error happens"

hdfs dfs -rm -r -skipTrash ${HDFS_OUTPUT_DIR}_tmp > /dev/null

hdfs dfs -cat ${HDFS_OUTPUT_DIR}/part-00000 | head -n $OUT_COUNT
