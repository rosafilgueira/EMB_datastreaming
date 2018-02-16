#!/usr/bin/env python

import requests
import os 
import sys
from time import sleep

url = 'http://localhost:8000/emb'

path="./EMB3_dataset_2017/"
sensor_id = 'emb3'

for filename in os.listdir(path):
    sensor = str.encode(sensor_id + ',')
    with open(path+filename, 'rb') as fd:
        for line in fd:
            line_n = sensor + line
            print("new line to send %s" % line_n)
            response = requests.post(url, data=line_n, headers={"Content-Type": "application/json"})
 	    print(response)
            sleep(1)
