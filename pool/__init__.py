from celery import Celery

app = Celery('pool')
app.config_from_object('pool.config')