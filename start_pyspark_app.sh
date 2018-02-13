set -e
# requirement for elasticsearch
#sudo sysctl -w vm.max_map_count=262144

# launch kafka, mqhub service in the background before starting the pyspark app
#docker-compose up -d


# parsing the filtered data


sudo docker-compose run --workdir="/app/" spark-master spark-submit --verbose --master spark://spark-master:7077 --jars /app_dependencies/spark-streaming-kafka-0-8-assembly_2.11-2.2.0.jar,/app_dependencies/elasticsearch-hadoop-5.0.0.jar,/app_dependencies/kafka_2.10-0.8.2.2.jar,/app_dependencies/kafka-clients-0.8.2.2.jar,/app_dependencies/metrics-core-2.2.0.jar  --conf spark.io.compression.codec=lz4 /app/integration_emb_spark_app.py --zq zookeeper:2181 --topic emb --checkpoint ./ --es_host elasticsearch --es_port 9200 --output /test_output/streaming_output/emb


