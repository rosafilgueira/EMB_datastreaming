import sys
from time import sleep
from kafka import KafkaProducer

def main():
    data = sys.argv[1]
    topic = sys.argv[2]
    sensor_id = str.encode(sys.argv[3] + ',')
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    with open(data, 'rb') as fd:
        for line in fd:
            line_n = sensor_id + line
            print("new line to send %s" % line_n)
            producer.send(topic, line_n)
            sleep(3)


if __name__=="__main__":
    main()
