#!/usr/bin/env python


#python sensor-simulator.py -s emb3

import argparse
import requests
import os 
import sys
from time import sleep

url = 'http://localhost:8000/emb'

 
s_help = 'sensor to simulate, e.g. emb3' 
description = 'Sensor id is required (-s is required).'
parser = argparse.ArgumentParser(description = description)
parser.add_argument("-s", help=s_help)
args = parser.parse_args()

sensor_id = args.s
path= "./"+sensor_id.upper()+"_dataset_2017/"

print ("path is %s" % path)

for filename in os.listdir(path):
    sensor = str.encode(sensor_id + ',')
    with open(path+filename, 'rb') as fd:
        for line in fd:
            line_n = sensor + line
            print("new line to send %s" % line_n)
            response = requests.post(url, data=line_n, headers={"Content-Type": "application/json"})
 	    print(response)
            sleep(3)
