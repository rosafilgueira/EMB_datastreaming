from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

def saveToES(rdd, es_conf):
    rdd_es = rdd.map(lambda x: [e for e in x]).map(lambda e: json.dumps({'date': e[0], 'time': e[1], 'sec':int(e[2]), 'ph':float(e[3]), 'water_level':float(e[4]), 'water_temp':float(e[5]), 'tdg':int(e[6].split("\r")[0])})).map(lambda x: ('id', x))
    print("cleaned rdd %s" % rdd_es.collect())	

    rdd_es.saveAsNewAPIHadoopFile(
        path="-",
        outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
        keyClass="org.apache.hadoop.io.NullWritable",
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", conf=es_conf)

    print("-------> After save to elasticsearch %s" % rdd_es.collect())	
    return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='kafka-spark-streaming-elasticsearch integration test')
    parser.add_argument('--zq', default='zookeeper:2181', required=True)
    parser.add_argument('--topic', default='emb', required=True)
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--es_host', default='elasticsearch', required=True)
    parser.add_argument('--es_port', default='9200', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    es_conf = {"es.nodes": args.es_host,
               "es.port": args.es_port,
               "es.resource": '/'.join(['emb_test', 'emb']),
               "es.input.json": "true",
               "es.batch.size.entries": '100'}

    sc = SparkContext(appName="PythonStreamingKafkaEMB")
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint(args.checkpoint)
    print("-------> :args.output is %s" % args.output)

    zq= args.zq
    topic=args.topic
    print("------> topic is %s, and zq %s" % (topic, zq))
    kvs = KafkaUtils.createStream(ssc, zq, 'raw-event-streaming-consumer', {topic:1})
    lines = kvs.map(lambda x: x[1])
    values = lines.map(lambda line: line.split(","))
    values.pprint()
    values.saveAsTextFiles(args.output)
    values.foreachRDD(lambda x: saveToES(x, es_conf))
    ssc.start()
    ssc.awaitTermination()
