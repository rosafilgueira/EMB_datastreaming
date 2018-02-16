import falcon
import json
from falconjsonio.schema import request_schema
import falconjsonio.middleware
from kafka import KafkaProducer


class BdrResource:
    def on_post(self, req, resp):
	msg = json.dumps(req.context['doc'], encoding='utf-8')
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('emb', msg)
        producer.flush()
        resp.status = falcon.HTTP_201
        resp.body = msg

class HealthCheckResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"healthcheck":"ok"}, encoding='utf-8')

app = falcon.API(
    middleware=[
        falconjsonio.middleware.RequireJSON(),
        falconjsonio.middleware.JSONTranslator(),
    ],
)

emb = BdrResource()
healthcheck = HealthCheckResource()

app.add_route('/emb', emb)
app.add_route('/healthcheck', healthcheck)
