set -x 
$SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi --master  
--master spark://129.114.108.142:7077 $SPARK_HOME/examples/jars/spark-examples_22
.11-2.2.0.jar 100
