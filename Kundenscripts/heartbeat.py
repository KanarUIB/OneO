import time
import re
import os
import requests
import string
from ctypes import windll
import subprocess
import random



# Globale Url des Management-Portals mit der subdirectory /heartbeat welche REST (POST) Abfragen bearbeitet
URL = "http://localhost:8000/heartbeat"




def searchFiles(dir : list, zaehler = 0):
    """
    Sucht mithilfe der Liste von Laufwerken nach dem Ordner 'Kundenscripts',
    in welchem sich die Dateien LOG.txt und congif.txt befinden

    Parameters:
        dir list:                           Liste aller existierenden Laufwerke des Clients (Bsp.: ['C','D'])
        zaehler int:                        Hilfsvariable für rekursiven Methodenaufruf mit anderem Root Ordner aus der dir list
    """

    global URL
    abspathLog = ""
    abspathConfig = ""

    for root, dirs, files in os.walk(dir[zaehler] + ":/"):
        if os.path.basename(root) != 'Kundenscripts':
            continue

        abspathLog = str(files[files.index('LOG.txt')])
        abspathConfig = str(files[files.index('config.txt')])
        path = open("path.txt", "w")
        path.write(os.path.abspath(root))
        path.close()
        break

    if not abspathLog and not abspathConfig:
        zaehler += 1
        if zaehler == len(dir):
            return
        searchFiles(dir, zaehler)

    # Speichert die zu sendenden Daten (lizenzschluessel und meldung) in PARAMS durch die Hilfsmethode readData()
    PARAMS = readData(str(os.path.abspath(root)), abspathLog, abspathConfig)


    # Sendet den Request an die Heartbeat API
    requests.post(url=URL, data=PARAMS)







def readData(dir: str, abspathLog: str, abspathConfig: str) -> dict:
    """
    Liest die Daten aus config.txt und LOG.txt aus und speichert sie im PARAMS dict

    Parameters:
        dir str:                           der absolute Pfad zu dem Root Ordner, in welchem sich der Lizenzschlüssel und die LOG Datei befinden
        abspathLog : str                   die LOG (.txt) Datei
        abspathConfig str:                 die config (.txt) Datei

    Returns:
        PARAMS dict:                       dictionary mit den Key-Value-Paaren lizenzschluessel und meldung mit den dazugehörigen Werten
    """

    if not dir or not abspathLog or not abspathConfig:
        return {}


    abspathLog = dir + "\\" + abspathLog
    abspathConfig = dir + "\\" + abspathConfig


    log = open(abspathLog, "r")
    meldung = str(log.read())
    log.close()

    pattern = "[0-2]{1}[0-9]{1}[:][0-5]{1}[0-9]{1}\s[0-3]{1}[0-9]{1}[.][0-1]{1}[0-9]{1}[.][2]{1}[0-1]{1}[0-9]{2}"
    meldung = re.findall(pattern + "\s[\[\]a-zA-Z0-9_ ]*", meldung)[-1]

    config = open(abspathConfig, "r")
    lizenz = config.read()
    config.close()

    PARAMS = {
        "lizenzschluessel": lizenz,
        "meldung": meldung
    }

    return PARAMS





def directRequest(dir: str):
    """ Sendet den Request an die Heartbeat API

    Parameters:
        dir str:                       der absolute Pfad zu dem Root Ordner, in welchem sich der Lizenzschlüssel und die LOG Datei befinden
    """

    PARAMS = readData(dir, "LOG.txt", "config.txt")
    requests.post(url= URL, data= PARAMS)



def get_drives() -> list :
    """
    Findet alle existierenden Laufwerke und speichert diese in drives[]

    Returns:
        drives list:                  Liste aller existierenden Laufwerke des Clients
    """

    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives







def execute():
    """ Führt den Heartbeat Request aus und prüft vorher ob path.txt einen Inhalt besitzt (den absoluten Pfad),
        um darauf basierend zwei verschiedene Wege zu gehen (searchFiles oder directRequest)
    """
    drives = get_drives()
    try:
        path = open("path.txt", "r")
        abspathPath = path.read()
        path.close()
    except FileNotFoundError:
        abspathPath = ""

    if not abspathPath:
        searchFiles(drives)
    else:
        directRequest(abspathPath)



# delay mithilfe einer Zufallsvariable um die Menge an eingehenden Requests zu verteilen (Load Performace)
zufall = random.uniform(10, 100)
time.sleep(zufall)

# Führt den Heartbeat-Request-Prozess aus
execute()


#Fürt die autostart.bat Datei aus um den Windows Task Scheduler zu registrieren (nur einmalig mithilfe des initial.txt)
firstTime = open("initial.txt", "r").read()
firstTime.replace("\n", "")
if firstTime.lower() == "false":
    subprocess.call([r'.\autostart.bat'])
    open("initial.txt", "w").write("True")




