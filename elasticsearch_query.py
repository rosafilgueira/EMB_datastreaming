import requests
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost', 'port':9200}])
response = requests.get('http://localhost:9200/emb_test')

print response

#res = es.get(index="emb_test", doc_type="emb", id="AWG46Yeq17_Xh6R0pg12")
#print res

res = es.search(index="emb_test", doc_type="emb", body={"query": {"match_all":{}}})
print res

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
	print("sensor_id %s - " % hit["_source"]["sensor_id"])


#u'sensor_id': u'"emb3', u'water_temp': 11.4, u'water_level': 28.26, u'tdg': 882, u'qc': u'normal', u'sec': 844, u'time': u'03:00:00', u'date': u'2017-01-03', u'ph': 7.21}




