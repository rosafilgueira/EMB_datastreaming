# UIs:
	Spark-Jobs: http://IP-address:4040
	Spark-Master: http://IP-address:8080
	Spark-Worker: http://IP-address:8081
	ElasticSearch: http://IP-address:9200
	Kibana: http://IP-address:5601


# Software

|Name	        |version               |
|---------------|:--------------------:|
|Elasticsearch	|6.2.2 (oss)           |
|Kibana 	|6.2.2 (oss)           |
|Kafka	        |0.10.2.0	       |
|Spark    	|2.2.0		       |
|Hadoop	        |1.1.0-hadoop2.8       |


# Use Case

![Figure use case](https://github.com/rosafilgueira/EMB_datastreaming/blob/master/Sensor-Figure.png)


# How to use EMB_datastreaming Hub


![Figure architecture](https://github.com/rosafilgueira/EMB_datastreaming/blob/master/data-streaming_hub.png )

(0.)  If you start from a 'clean'/'new' Centos7 VM --> You need to set up docker and docker-compose enviroment  



 For avoiding to introduce the password for docker/docker-compose commands, we recommend to create two Unix groups, one called docker and other called docker-compose (see notes from: note_add_sudo_docker.txt) and add users to it. 
  
  
  It is also recomendable to increase the virtual memory (requirement for elasticsearch)
  
  ```
    sysctl -w vm.max_map_count=262144
  ```

1. Upload the dockerized architecture-  (open a new tab - because the current one will be using for the docker-logs)

```
docker-compose up
```

2. Check if all the conatiners are up and running

```
docker-compose ps
```

3. Create the 'emb' topic for our application. Important: we recommend to use ./start_streaming_sensor.sh , which will save you to create the topic manually. Nevertheless, here you have the script for creating a topic 'manually'. 

```
./create-topic.sh kafka zookeeper:2181 emb
```

** Note: ./start_streaming_sensor.sh will do the steps 3 + 4.1 together  - Recommended option

4. Simulation of readings from sensors (we are going to stream data every 3 seconds but you can change the ratio of streaming). 
Start producing streams to the 'emb' topic - 1 stream per line and file. We have added the sensor_id to each line, so we know from which sensor the data is been streamed from.  There are two options - we recommend 4.1

* 4.1 Using websevices - Falcon (recommended option) - This option is included inside "start_streaming_sensor.sh".
  In a new terminal start a feeder script POSTing messages to Falcon. With -s you can indicate which sensor you want to stream data from.
  We have locally stored data from 'emb3' and 'emb2' sensors. 
  
  ```
  cd sensordata
  ./sensor-simulator.py -s emb3
  ```
  Falcoln sends the data to Kafka using a post request (you could check the post request in Falcoln/src/emb.py )

 
* 4.2 Using a python script:
  In a new terminal, type the following command to enter inside the spark-worker container:

  ```
  docker exec -it spark-worker bash
  ```
  Inside the container, the publish_emb.sh calls the producer_kafka.py to send data directly to Kafka (you could check pyspark_app/scripts   /producer_kakfa.py). You could change the publish_emb.sh script to stream data from a different sensor. By default, we have choosen emb3:
 
  ```
  cd /scripts
  ./publish_emb.sh
  ```

5. Check if the streams can be receive from the 'emb' topic

```
./receive-topic.sh kafka emb zookeeper:2181
```

6. Check if the elasticsearch has been correctly created -  
(open new tab - this one will be used for searching data in elasticsearch)

```
-index: emb_test
-type: emb
-fields:
        "sensor_id": {"type": "text"}, (Id of the sensor: e.g. emb2, emb3)
	date" : { "type" : "date", "format":"yyyy-MM-dd"} (UTC)
        "time" : { "type" : "date", "format": "HH:mm:ss"} (UTC)
        "sec": { "type" : "integer"} ->  (micro-siemens per centimetre) 
        "ph": { "type" : "float"}
        "water_level": { "type" : "float"} --> Water Level aOD (metre) 
        "water_temp": { "type" : "float"} --> Water Temperature (Celsius) 
	"tdg": { "type" : "integer"} -->  TDG (millibar) 
	"qc": {type:text} --> QualityControl 
	
```	

```
docker exec -it elasticsearch bash
```

Iniside the container

```
cd /opt/create-es-index
./check_index.sh
./check_values.sh
```

7. Start the apache spark application (locally option /master-cluster option) that receives streams from Kafka (listening 'emb' topic) and store them in elasticsearch (index emb_test, type: emb)
 
 ```
 docker exec -it spark-master bash
 ```
 
Two options to submit an application: 
7.A) Inside the container:
  
  ```
  7.A.1 cd /app/submit_scripts ( pyspark application is at /app)
  7.A.2 ./submit_emb_local.sh (locally version - ideal for testing) or ./submit_emb_spark.sh (master-cluster version - distributed)
  ```
7.B) Outside the container (using the master-cluster version) - Submiting an apache Spark appication to the Spark Master-cluster
 
  ```
  start_pyspark_app.sh
  ```
  
  You can always check the Spark UIs (8080, 8081, 4040, 4041) to check how the data is being streamed, and how the master and the workers perform. Here you have an example of the job history UI (ports 4040 or 4041 - depending if you have submitted the application with start_pyspark_app.sh (port 4041) or submit_emb_master.sh (port 4040))
  
  ![Figure streaming UI](https://github.com/rosafilgueira/EMB_datastreaming/blob/master/spark-straming-UI2.png)

 8. Checking/Getting data/values Elastisearch:

 Two options:

   Outside the container (recommended):
   
   ```
   python elasticsearch_query.py
   ```

   Inside the elasticsearch container:
	
  ```
   docker exec -it elasticsearch bash
   cd /opt/create-index
   ./check_values.sh
  ```
	
9. Exploring you data in Kibana:

Open a browser and type: http://IP-address:5601. You have several options to visualize your data from elasticsearch.

![Figure kibana](https://github.com/rosafilgueira/EMB_datastreaming/blob/master/kibana-screenshot.png)



