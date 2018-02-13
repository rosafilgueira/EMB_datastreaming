#!/bin/bash
set -x 

# sudo docker ps -a 

# ./receive-topic.sh kafka emb zookeeper:2181
sudo docker exec -i $1 /opt/kafka_2.12-1.0.0/bin/kafka-console-consumer.sh --topic=$2 --zookeeper=$3

