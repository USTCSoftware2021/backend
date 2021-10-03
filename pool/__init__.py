from celery import Celery
from redis import Redis

app = Celery('pool')
app.config_from_object('pool.config')

hash_redis = Redis("localhost", port=6379, db=1)