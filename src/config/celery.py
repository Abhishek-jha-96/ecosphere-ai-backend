from celery import Celery
from config.base import Settings


app = Celery("ecosphere", broker=Settings.REDIS_URL)
