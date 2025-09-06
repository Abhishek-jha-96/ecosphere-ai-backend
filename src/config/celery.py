from celery import Celery

# from celery.schedules import crontab
from config.base import settings


print("broker url", settings.REDIS_URL)
app = Celery("ecosphere", broker=settings.REDIS_URL)


# app.conf.beat_schedule = {
#     "add-every-30-seconds": {
#         "task": "tasks.add",
#         "schedule": crontab(hour=7, minute=30, day_of_week=1),
#         "args": (16, 16),
#     },
# }
