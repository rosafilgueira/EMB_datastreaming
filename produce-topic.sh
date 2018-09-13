#!/bin/bash
set -x 

#./produce-topic.sh kafka kafka:9092 word_count pyspark_app/data/word_count.txt
docker exec -i $1 /opt/kafka_2.11-2.0.0//bin/kafka-console-producer.sh --broker-list $2 --topic $3 < $4

