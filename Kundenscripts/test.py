import schedule
import time
from datetime import datetime
import re

def task():
    dateNow = datetime.now().strftime("Day{%d}:Month{%m}:Year{%y}|Hour{%H}:Minute{%M}")
    print(re.match("Day",dateNow).match())



schedule.every(1).seconds.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)