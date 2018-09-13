#!/bin/bash
set -x 

# sudo docker ps -a 

# ./receive-topic.sh kafka emb zookeeper:2181
docker exec -i $1 /opt/kafka_2.11-2.0.0/bin/kafka-console-consumer.sh --topic=$2 --zookeeper=$3

