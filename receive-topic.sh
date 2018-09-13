#!/bin/bash
set -x 

# sudo docker ps -a 

# ./receive-topic.sh
sudo docker exec -i kafka /opt/kafka_2.11-2.0.0/bin/kafka-console-consumer.sh --topic=emb3 --bootstrap-server=kafka:9092

