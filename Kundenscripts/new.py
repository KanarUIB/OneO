from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.jobstores.mongodb import MongoDBJobStore
#from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def job():
    print("test")

"""
jobstores = {
    'mongo': MongoDBJobStore(),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
"""
#scheduler = BackgroundScheduler(jobstores="default", executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler = BackgroundScheduler(daemon=True)

scheduler.add_job(lambda: scheduler.print_jobs(), 'interval', seconds=5)
scheduler.start()