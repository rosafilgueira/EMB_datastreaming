# UIs:
	Hadoop: http://192.5.87.53:50070/
	Datanode: http://192.5.87.53:50075
	Spark-Jobs: http://192.5.87.53:4040
	Spark-Notebook: http://192.5.87.53:8888
	Spark-Master: http://192.5.87.53:8080
	Spark-Worker: http://192.5.87.53:8081
	ElasticSearch: http://192.5.87.53:9200
	Kibana: http://192.5.87.53:5601
	Hue: http://192.5.87.53:8088


# Software

|Name	        |version               |
|---------------|:--------------------:|
|Elasticsearch	|5                     |
|Kafka	        |0.10.2.0	       |
|Spark    	|2.2.0		       |
|Hadoop	        |1.1.0-hadoop2.8       |

# How to use DataStreaming Hub

0. To set up docker and docker-compose enviroment in the Centos7 VM  

```
   ./config.sh 

```

1. >> sudo docker-compose up
 DESCRIPTION: upload the dockerized architecture 	
 (open a new tab - because the current one will be using for the docker-logs)

2. >> sudo docker-compose ps
 DESCRIPTION: check if all the conatiners are up and running

3. >> /create-topic.sh kafka zookeeper:2181 emb
 DESCRIPTION: create the 'emb' topic for our application 

4. >> sudo docker exec -it spark-worker bash
 DESCRIPTION: start to produce streams of EMB data to the 'emb' topic - 1 stream per line and file	
	Inside the container:
	 4.1 >> cd /scripts
	 4.2 >> ./publish_emb.sh

  (open a new tab - this one will be used for producing the streams to 'emb' topic)

5. >> ./receive-topic.sh kafka emb zookeeper:2181
 DESCRIPTION: check if the streams can be receive from the 'emb' topic

6. >>  sudo docker exec -it elasticsearch bash
  DESCRIPTION: check if the elasticsearch has been correctly created 
     Iniside the container:
	6.1 >> cd /opt/create-index
	6.2 >> ./check_index.sh
	6.3 >> ./check_values.sh

 (open new tab - this one will be used for searching data in elasticsearch)

 7. >> sudo docker exec -it spark-master bash
 DESCRIPTION: Start the apache spark application (locally/cluster) that receives stream from Kafka and store them in elasticsearch

  Inside the container:
	7.1 >> cd /app/submit_scripts ( pyspark application is at /app)
	7.2 >> ./submit_emb_local.sh  or ./submit_emb_spark.sh


8. Inside the elasticsearch container
	8.1 >> ./check_values.sh

9. >> start_pyspark_app.sh
  DESCRIPTION: Submit the spark application from outside the spark-master container (using the 'cluster' version)


10. >>  curl -XGET '192.171.148.207:9200/emb_test/_mapping/emb?pretty=1'
  DESCRIPTION: Check elastic search from outside the elastic container	
	


