#!/bin/bash
set -x 


./create-topic.sh kafka zookeeper:2181 emb
cd sensordata
python sensor-simulator.py -s emb3
