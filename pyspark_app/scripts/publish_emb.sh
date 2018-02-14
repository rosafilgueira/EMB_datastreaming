#!/bin/bash
set -x

for file in ./EMB3_dataset_2017 /*
do
  echo "New $file to stream"
  python producer_kafka.py $file 'emb' 'emb3'
  
done



