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

1. To set up docker and docker-compose enviroment in the Centos7 VM  

```
   ./config.sh 

```
 
2. Edit `docker-compose.yml` file and replace paths in `volumes` to match your environment

3. To start the datastreaming hub: Kafka + Spark + HDFS + ElasticSearch + Cassandra:
```
    docker-compose up -d
```
Note: if you have previously run this command perhaps you will need to delete:
sudo rm -rf data/namenode/

4. To scale up spark-workers:
```
    docker-compose scale spark-worker=3
```

5. To create a topic (replace the kafka_container (e.g. docker-compose ps) and IP addrees with yours):
```
    ./create-topic.sh datastreaminghub_kafka_1 192.5.87.53:2181 word_count
```

6. To produce a topic (replace the kafka_container (e.g. docker-compose ps) and IP addrees with yours):
```
./produce-topic.sh datastreaminghub_kafka_1 192.5.87.53:9092 word_count pyspark_app/data/word_count.txt
```
    or 
```
./produce-topic-interactive.sh datastreaminghub_kafka_1 192.5.87.53:9092 word_count
> adff 
> dfdfadfdaf
```
   or
```
sudo docker exec -it $(sudo docker-compose ps -q kafka) kafka-console-producer.sh --broker-list 192.5.87.53:9092 --topic word_count
```

7. To receive a topic (replace the kafka_container (e.g. docker-compose ps) and IP addrees with yours):
```
    ./receive-topic.sh datastreaminghub_kafka_1 word_count 192.5.87.53:2181
```

8. To submit spark jobs:
* option 1 -Submitting locally a simple example: SparkPI:
```
docker exec -it spark-master bash
cd /submit_scripts
./submit_local.sh
```
* option 2 - Submitting to the standalone cluster (simple example pi.py):
```
docker exec -it spark-master bash
cd /submit_scripts
./submit_master_simple.sh
```
* option 3 - Submitting to the standalone cluster a kafka+spark application (kafkawordcount.py):
```
docker exec -it spark-master bash
cd /submit_scripts
./submit_master_kafka_2.sh
```

* option 4 - submit a spark + kafka example:
```
./start_pyspark_app.sh
```

### Option 3 and 4 submit two spark jobs that retrieve data from kafka, processes it, and then save the output to elasticsearch.

As follows you have the instructions to run them:

* First of all, before you start, check if your system satisfy elasticsearch docker prerequisite: `vm.max_map_count` sysctl must be set to at least 262144.
```bash
sudo sysctl -w vm.max_map_count=262144
```
with this setting, elasticsearch container could start and run normally.
* Secondly, start kafka, elasticsearch services. Note that in our test, a topic ‘word-count’ in kafka and an index ‘es_test’ as well as a type ‘word_count’ in elasticsearch are automatically created, I’ll explain how they are created in the next section.
```bash
docker-compose up
```
* Start publishing data to kafka from Spark worker (open a terminal)
```
./create-topic.sh datastreaminghub_kafka_1 192.5.87.53:2181 word_count

docker exec -it datastreaminghub_spark-worker_1 bash
cd /scripts
./publish-raw-data.sh
```

* Check that we are receiving data (open a terminal):
```
    ./receive-topic.sh datastreaminghub_kafka_1 word_count 192.5.87.53:2181
```
* Start the spark streaming application with the OPTION 3 or OPTION 4

* Check data insertion

Once you see the output printed on the screen and inserted into elasticsearch, we may check for confirmation whether the documents have been inserted successfully.
```bash
docker exec -it datastreaminghub_spark-worker_1 bash
```
A simple query for counting the number of inserted documents:
```bash
curl -XGET 'elasticsearch:9200/es_test/word_count/_count?pretty' -d '                                                                                    
{
  "query":{ 
  "match_all":{}
  }
}'
```
If you get the following response, congratulations !  you made this integration test work!
```bash
{
  "count" : 135,
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  }
}
```
* Lastly, tear down all the services
```bash
docker-compose down
```




9. Notebook: Go to the browser and use Notebook UI (http://192.5.87.53:8888). And you can check your Spark enviroment with the Simple_App notebook. 


## Application for making product recommendations  for an imaginary e-commerce store. 

It is written in Python and employs Kafka, Spark (in Jupyter notebook), Cassandra and Falcon.
All the components are tied in with Docker and their relationships are captured in `docker-compose`.   


* Create 'bdr' topic:
```
	./create-topic.sh datastreaminghub_kafka_1 192.5.87.53:2181 bdr
```
* Simulation of user clicks/actions
  * In a terminal, go to the `mydata` folder and start a feeder script POSTing JSON messages to Falcon: `./user-simulator.py`
  * The clicks (every line of the json file) are sent as a post-request to the webservices, which are forward to the Kafka. 

* Note: You now can check if you receive data from 'bdr' topic, opening a new terminal:
```
    ./receive-topic.sh datastreaminghub_kafka_1 bdr 192.5.87.53:2181
```
* Cassandra  
  * In another terminal, connect to Cassandra instance with command like:
  `docker exec -it datastreaminghub_cassandra_1 bash`
     * Once inside, initialise Cassandra's keyspace: `cqlsh -f bdr/init.sql`
     * You can also run `cqlsh` and start issuing CQL statements directly against Cassandra
* Spark Notebook
  * In a browser, navigate to `http://192.5.87.53:8888/` and choose `Lambda - Stream - Users who bought X also bought`.
  Shift+Enter all the cells or choose from the top menu: Cell->Run All
    *Lambda Stream also stores results in cassandra. So, the batch notebook ( which does not use kafka), check the cassandra events, and does the recommendations.

  * Once Spark Streaming is running and the data feeder is started, you should see the recommendation table become populated in Cassandra
  * Repeat the same for other notebooks if required: Note (execute first streaming, then batch for the Lambda option)
    * `Lambda - Batch- Users who bought X also bought`
    * `Kappa - Users who bought X also bought`
    * `Kappa - Collaborative Filtering`
  * Note: Lambda does not 'listen' to Kafka, and uses casanda table for doing the recommendation. 

* Falcon
  * Once every gear is in motion, you can finally get the recommendations. Open a browser (or otherwise issue GET request) 
  to hit Falcon and get recommendations like this: 
    * Lambda: `http://192.5.87.53:8000/bdr?product-lambda=59` should return response like `{"product":59, "recommendedProducts":[29,49,99,19,62]}`
    * Kappa: `http://192.5.87.53:8000/bdr?product-kappa=41` should return response like `{"product":41, "recommendedProducts":[21,5,95,83,37]}`
    * Kappa Collaborative Filtering user customised recommendation: `http://192.5.87.53:8000/bdr?user=2105` with response like 
    `{"user":2105, "recommendedProducts":[77,5,95,83,37]}`

* Casandra:
   * To check the results in the casandra container:
	`docker exec -it datastreaminghub_cassandra_1 bash`
	`cqlsh`
	`use bdr;`
	`select * from top_other_products_batch;`
	`select * from top_other_products_stream;`
	`select * from top_other_products_kappa;`


##Docker on VM
If your disk has a very limited capacity or you run docker on a virtual machine, hopefully you may find the following section quite useful.

1. Delete all containers:
```bash
docker ps -a | grep 'ago' | awk '{print $1}' | xargs --no-run-if-empty docker rm
```
2. Untagged images:
when you use `docker images` to display all the images in your system, if you find some weird ones like <none><none>, the post [What are Docker <none>:<none> images?](http://www.projectatomic.io/blog/2015/07/what-are-docker-none-none-images/) is worth a read.
