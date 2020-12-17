import schedule
import time
from datetime import datetime
import re
import os
import hashlib
import requests


URL = "http://localhost:8000/heartbeat"



def task():
    global URL
    #dateNow = datetime.now().strftime("Day{%d}:Month{%m}:Year{%y}|Hour{%H}:Minute{%M}")
    #print(re.match("[a-z*A-Z]", dateNow))

    """
    os.walk()Crawlt durch alle Ordner des Rechners
    """
    for root, dirs, files in os.walk('D:/'):
        print(root)
        if os.path.basename(root) != 'Kundenscripts':
            continue


        abspathLog = str(os.path.abspath(root)) + "\\" + str(files[files.index('LOG.txt')])


        abspathConfig = str(os.path.abspath(root)) + "\\" + str(files[files.index('config.txt')])

        break



    log = open(abspathLog, "r")
    meldung = str(log.read())
    log.close()

    pattern = "[0-2]{1}[0-9]{1}[:][0-5]{1}[0-9]{1}\s[0-3]{1}[0-9]{1}[.][0-1]{1}[0-9]{1}[.][2]{1}[0-1]{1}[0-9]{2}"
    meldung = re.findall(pattern + "\s[\[\]a-zA-Z0-9_ ]*", meldung)[-1]


    config = open(abspathConfig, "r")
    lizenz = config.read()
    config.close()


    encrypted = hashlib.sha256('1234').hexdigest()
    print(encrypted)

    PARAMS = {
        "lizenzschluessel": lizenz,
        "meldung": meldung
    }

    print(PARAMS)

    #requests.post(url=URL, data=PARAMS)


schedule.every(1).seconds.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)
