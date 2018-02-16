#!/bin/bash
set -x

for file in ./test/*
do
  echo "New $file to stream"
  python producer_kafka.py $file 'emb' 'emb3'
  
done



