#!/bin/bash
set -x 

# sudo docker ps -a 

# ./receive-topic.sh kafka emb
sudo docker exec -i $1 /opt/kafka_2.11-2.0.0/bin/kafka-console-consumer.sh --topic=$2 --bootstrap-server=kafka:9092

