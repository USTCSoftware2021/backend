
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 1
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = (
    'pool.tasks'
)
