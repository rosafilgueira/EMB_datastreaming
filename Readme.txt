1. >> sudo docker-compose up
 DESCRIPTION: upload the dockerized architecture 	
 (open a new tab - because the current one will be using for the docker-logs)

2. >> sudo docker-compose ps
 DESCRIPTION: check if all the conatiners are up and running
     Name                   Command               State                               Ports
-----------------------------------------------------------------------------------------------------------------------
datanode         /entrypoint.sh /run.sh           Up      0.0.0.0:50075->50075/tcp
elasticsearch    /docker-entrypoint.sh supe ...   Up      0.0.0.0:9200->9200/tcp, 9300/tcp
kafka            start-kafka.sh                   Up      0.0.0.0:9092->9092/tcp
namenode         /entrypoint.sh /run.sh           Up      0.0.0.0:50070->50070/tcp
spark-master     bin/spark-class org.apache ...   Up      0.0.0.0:4040->4040/tcp, 0.0.0.0:6066->6066/tcp, 7002/tcp,
                                                          7003/tcp, 7004/tcp, 7005/tcp, 7006/tcp,
                                                          0.0.0.0:7021->7021/tcp, 0.0.0.0:7077->7077/tcp,
                                                          0.0.0.0:8080->8080/tcp
spark-notebook   tini -- start-notebook.sh  ...   Up      0.0.0.0:8888->8888/tcp
spark-worker     bin/spark-class org.apache ...   Up      0.0.0.0:7011->7011/tcp, 7012/tcp, 7013/tcp, 7014/tcp,
                                                          7015/tcp, 7016/tcp, 0.0.0.0:8081->8081/tcp, 8881/tcp
zookeeper        /bin/sh -c /usr/sbin/sshd  ...   Up      0.0.0.0:2181->2181/tcp, 22/tcp, 2888/tcp, 3888/tcp

3. >> /create-topic.sh kafka zookeeper:2181 emb
 DESCRIPTION: create the 'emb' topic for our application 
+ sudo docker exec -i kafka /opt/kafka_2.12-1.0.0/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic emb
Created topic "emb".

4. >> sudo docker exec -it spark-worker bash
 DESCRIPTION: start to produce streams of EMB data to the 'emb' topic - 1 stream per line and file	
	Inside the container:
	 4.1 >> cd /scripts
	 4.2 >> ./publish_emb.sh

  (open a new tab - this one will be used for producing the streams to 'emb' topic)

5. >> ./receive-topic.sh kafka emb zookeeper:2181
 DESCRIPTION: check if the streams can be receive from the 'emb' topic
  2017-01-02,01:00:00,844,7.21,28.23,11.4,881
  2017-01-02,02:00:00,844,7.21,28.23,11.4,881

6. >>  sudo docker exec -it elasticsearch bash
  DESCRIPTION: check if the elasticsearch has been correctly created 
     Iniside the container:
	6.1 >> cd /opt/create-index
	6.2 >> ./check_index.sh
{
  "emb_test" : {
    "mappings" : {
      "emb" : {
        "_all" : {
          "enabled" : true
        },
        "properties" : {
          "date" : {
            "type" : "date",
            "format" : "yyyy-MM-dd"
          },
          "ph" : {
            "type" : "float"
          },
          "sec" : {
            "type" : "integer"
          },
          "tdg" : {
            "type" : "integer"
          },
          "time" : {
            "type" : "date",
            "format" : "hh:mm:ss"
          },
          "water_level" : {
            "type" : "short"
          },
          "water_temp" : {
            "type" : "short"
          }
        }
      }
    }
  }
}
	6.3 >> ./check_values.sh
{
  "took" : 4,
  "timed_out" : false,
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 0,
    "max_score" : null,
    "hits" : [ ]
  }
}

 (open new tab - this one will be used for searching data in elasticsearch)

 7. >> sudo docker exec -it spark-master bash
 DESCRIPTION: Start the apache spark application (locally/cluster) that receives stream from Kafka and store them in elasticsearch

  Inside the container:
	7.1 >> cd /app/submit_scripts ( pyspark application is at /app)
	7.2 >> ./submit_emb_local.sh  or ./submit_emb_spark.sh



8. Inside the elasticsearch container
	8.1 >> ./check_values.sh
{
  "took" : 39,
  "timed_out" : false,
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "emb_test",
        "_type" : "emb",
        "_id" : "AWGLBFZfdgrI96o9CjeT",
        "_score" : 1.0,
        "_source" : {
          "tdg" : 882,
          "water_temp" : 11.4,
          "sec" : 844,
          "water_level" : 28.24,
          "date" : "2017-01-04",
          "time" : "10:00:00",
          "ph" : 7.23
        }
      }
    ]
  }
}
 


9. >> start_pyspark_app.sh
  DESCRIPTION: Submit the spark application from outside the spark-master container (using the 'cluster' version)


10. >>  curl -XGET '192.171.148.207:9200/emb_test/_mapping/emb?pretty=1'
  DESCRIPTION: Check elastic search from outside the elastic container	
	
