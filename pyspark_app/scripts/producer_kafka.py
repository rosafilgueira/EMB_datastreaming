import sys
from time import sleep
from kafka import KafkaProducer

def main():
    data = sys.argv[1]
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    with open(data, 'rb') as fd:
        for line in fd:
            print("line to send %s" % line)
            producer.send('emb', line)
            sleep(10)


if __name__=="__main__":
    main()
