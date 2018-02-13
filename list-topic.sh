#!/bin/bash

# sudo docker ps -a 
#./list-topic.sh dockersparkkafkastreaming_kafka_1 129.114.108.142:2181

sudo docker exec -i $1 /opt/kafka/bin/kafka-topics.sh --list --zookeeper $2
