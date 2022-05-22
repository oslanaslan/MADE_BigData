#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
INPUT_NAME=${1}
OUTPUT_NAME=${2}
JOB_NAME=${3}

hdfs dfs -rm -r -skipTrash $OUTPUT_NAME > /dev/null

yarn jar $HADOOP_STREAMING_JAR \
	-files mapper.py,reducer.py \
	-D mapreduce.job.name=$JOB_NAME \
	-numReduceTasks 2 \
	-mapper 'python3 mapper.py' \
	-reducer 'python3 reducer.py' \
	-input $INPUT_NAME \
	-output $OUTPUT_NAME > /dev/null

hdfs dfs -cat $OUTPUT_NAME/part-00000 | head -n 50 

