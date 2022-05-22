#!/usr/bin/env bash

INPUT_PATH="/data/stackexchange_part/posts/Posts.xml"
OUTPUT_PATH="/user/bdmade2022q2_ashabokov/hw03_mr_advanced_output.out"
JOB_NAME="ashabokov_task_3"
STDOUT_FILE="output.out"

./run.sh $INPUT_PATH $OUTPUT_PATH $JOB_NAME > $STDOUT_FILE

