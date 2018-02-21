import requests
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost', 'port':9200}])
response = requests.get('http://localhost:9200/emb_test')

print response

#res = es.get(index="emb_test", doc_type="emb", id="AWG46Yeq17_Xh6R0pg12")
res = es.search(index="emb_test", doc_type="emb", body={"query": {"match_all":{}}})
print("Got %d elements:" % res['hits']['total'])
for hit in res['hits']['hits']:
	print("sensor_id:%(sensor_id)s, date-time: %(date)s %(time)s -- water_temp: %(water_temp)s, water_level: %(water_level)s, ph: %(ph)s, tdg: %(tdg)s, sec: %(sec)s -- quality check: %(qc)s" % hit["_source"])






