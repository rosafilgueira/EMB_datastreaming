set -x 
$SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi --master spark://192.5.87.53:7077 --deploy-mode cluster --supervise $SPARK_HOME/examples/jars/spark-examples_2.11-2.2.0.jar 100
