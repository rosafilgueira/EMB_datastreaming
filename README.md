# UIs:
	Hadoop: http://IP-address:50070/
	Datanode: http://IP-address:50075
	Spark-Jobs: http://IP-address:4040
	Spark-Notebook: http://IP-address:8888
	Spark-Master: http://IP-address:8080
	Spark-Worker: http://IP-address:8081
	ElasticSearch: http://IP-address:9200
	Kibana: http://IP-address:5601


# Software

|Name	        |version               |
|---------------|:--------------------:|
|Elasticsearch	|5                     |
|Kafka	        |0.10.2.0	       |
|Spark    	|2.2.0		       |
|Hadoop	        |1.1.0-hadoop2.8       |


# Use Case

![Figure use case](https://github.com/rosafilgueira/EMB_datastreaming/blob/master/Sensor-Figure.png)


# How to use EMB_datastreaming Hub


![Figure architecture](https://github.com/rosafilgueira/EMB_datastreaming/blob/master/data-streaming_hub.png )

(0.)  If you start from a 'clean'/'new' Centos7 VM --> You need to set up docker and docker-compose enviroment  

```
   ./config.sh 

```

1. Upload the dockerized architecture-  (open a new tab - because the current one will be using for the docker-logs)

```
 sudo docker-compose up
```

2. Check if all the conatiners are up and running

```
sudo docker-compose ps
```

3. Create the 'emb' topic for our application 

```
./create-topic.sh kafka zookeeper:2181 emb
```

4. Simulation of readings from sensors. 
Start producing streams to the 'emb' topic - 1 stream per line and file. We have added the sensor_id to each line, so we know from which sensor the data is been streamed from. 

* 4.1 Using websevices - Falcon (recommended option):
  In a new terminal start a feeder script POSTing messages to Falcon. With -s you can indicate which sensor you want to stream data from:
  
  ```
  cd sensordata
  ./sensor-simulator.py -s emb3
  ```
  Falcoln sends the data to Kafka using a post request (you could check the post request in Falcoln/src/emb.py )

 
* 4.2 Using a python script:
  In a new terminal, type the following command to enter inside the spark-worker container:

  ```
  sudo docker exec -it spark-worker bash
  ```
  Inside the container, the publish_emb.sh calls the producer_kafka.py to send data directly to Kafka (you could check pyspark_app/scripts   /producer_kakfa.py):
 
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
	date" : { "type" : "date", "format":"yyyy-MM-dd"}
        "time" : { "type" : "date", "format": "HH:mm:ss"}
        "sec": { "type" : "integer"}
        "ph": { "type" : "float"}
        "water_level": { "type" : "float"}
        "water_temp": { "type" : "float"}
	"tdg": { "type" : "integer"}
	"qc": {type:text}
	
```	

```
sudo docker exec -it elasticsearch bash
```

Iniside the container

```
cd /opt/create-index
./check_index.sh
./check_values.sh
```

7. Start the apache spark application (locally option /master-cluster option) that receives streams from Kafka (listening 'emb' topic) and store them in elasticsearch (index emb_test, type: emb)
 
 ```
 sudo docker exec -it spark-master bash
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

 8. Checking/Getting data/values Elastisearch:

 Two options:
   Inside the elasticsearch container:
	
  ```
   sudo docker exec -it elasticsearch bash
   cd /opt/create-index
   ./check_values.sh
  ```
	
 Outside the container: 
	
```
curl -XGET 'locahost:9200/emb_test/_mapping/emb?pretty=1'
```
  Or you could run the examples_elasticsearch_querires
	


