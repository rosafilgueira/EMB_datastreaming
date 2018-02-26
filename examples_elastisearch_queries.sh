
#curl -XGET 'http://localhost:9200/emb_test/emb/_search?q=%2Bsensor_id:emb3%20%2Bsec:844' -H 'Content-Type: application/json'

#curl -XGET 'http://localhost:9200/emb_test/emb/_search?pretty' -H 'Content-Type: application/json' -d'
#{
#	"query":{
#		"range":{
#		   "date":{
#			"gt": "2016-12-01",
#			"lt": "2017-01-10"
#			}
#		      }
#	}
#
#}'

curl -XGET 'http://localhost:9200/emb_test/emb/_search?q=sensor_id:emb3%20pretty' -H 'Content-Type: application/json' -d'
{
	"query":{
		"range":{
		   "date":{
			"gte": "2017-01-01",
			"lte": "2017-01-10"
			}
		      }
	}

}'

