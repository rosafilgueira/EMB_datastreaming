#!/bin/bash
set -x 

#./produce-topic-interactive.sh kafka kafka:9092 word_count 
docker exec -i $1 /opt/kafka_2.12-1.0.0/bin/kafka-console-producer.sh --broker-list $2 --topic $3

