import os
import requests
import string
from ctypes import windll
import json
import subprocess
import random
import time


#Globale Url des Management-Portals mit der subdirectory /heartbeat welche REST (POST) Abfragen bearbeitet
URL = "http://localhost:8000/lizenzheartbeat"



def searchFiles(dir: list, zaehler = 0):
    """
    Crawlt die Laufwerke des Clients durch um den Ordner Kundenscripts zu finden, in welchem sich die notwendigen Dateien befinden

    Parameters:
        dir (list):                            Root Ordner von dem aus angefangen wird nach dem /Kundenscripts subordner zu suchen (Laufwerke des Clients)
        zaehler (int):                        Hilfsvariable für rekursiven Methodenaufruf mit anderem Root Ordner
    """
    global URL
    abspathConfig = ""

    if zaehler == 2:
        return
    for root, dirs, files in os.walk(dir[zaehler] + ":/"):
        if os.path.basename(root) != 'Kundenscripts':
            continue

        abspathConfig = str(files[files.index('config.txt')])
        path = open("./path.txt", "w")
        path.write(os.path.abspath(root))
        path.close()
        break

    if not abspathConfig:
        searchFiles("D:/", zaehler + 1)

    PARAMS = readData(str(os.path.abspath(root)), abspathConfig)


    requests.post(url=URL, data=PARAMS)



def readData(dir: str, abspathConfig: str) -> dict:
    """
    Liest den Lizenzschlüssel aus config.txt und speichert sie im PARAMS dict

    Parameters:
        dir (str):                           der absolute Pfad zu dem Root Ordner, in welchem sich der Lizenzschlüssel befindet
        abspathConfig (str):                 die config (.txt) Datei mit dem Lizenzschlüssel

    Returns:
        PARAMS (dict):                       dictionary mit den Key-Value-Paaren für lizenzschluessel mit dem dazugehörigen Wert
    """

    if not dir or not abspathConfig:
        return {}


    abspathConfig = dir + "\\" + abspathConfig

    config = open(abspathConfig, "r")
    lizenz = config.read()
    config.close()

    PARAMS = {
        "lizenzschluessel": lizenz
    }

    return PARAMS



def directRequest(dir: str):
    """
    Sendet den Request an die Lizenz API

    Parameters:
        dir (str):                      der absolute Pfad zu dem Root Ordner, in welchem sich der Lizenzschlüssel befindet
    """

    PARAMS = readData(dir, "config.txt")
    x = requests.post(url= URL, data= PARAMS)
    save = overwrite(json.loads(x.json()))

    requests.post(url="http://localhost:8000/lizenzheartbeat/lizenzsave", data=save)



def get_drives() -> list:
    """
    Findet alle existierenden Laufwerke und speichert diese in drives[]

    Returns:
        drives (list):                   Liste aller existierenden Laufwerke des Clients
    """

    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives



def execute():
    """
    Führt den Heartbeat Request aus und prüft vorher ob path.txt einen Inhalt besitzt (den absoluten Pfad),
    um darauf basierend zwei verschiedene Wege zu gehen (searchFiles oder directRequest)
    """
    drives = get_drives()
    try:
        path = open("./path.txt", "r")
        abspathPath = path.read()
        path.close()
    except FileNotFoundError:
        abspathPath = ""

    if not abspathPath:
        searchFiles(drives)
    else:
        directRequest(abspathPath)




def overwrite(lizenz):
    """
    Öffnet die Config-Datei, leert diese und fügt den neuen Lizenzschlüssel ein

    Parameters:
        lizenz (dict):                dictionary mit den Key-value Paaren für den alten und neuen Lizenzschlüssel sowie einer boolschen Hilfsvariable
    """
    overwrite = False
    old = ""
    new = ""

    if lizenz["exist"] == True:
        try:
            config = open("./config.txt", "r")
            old = config.read()
            config.close()

            config = open("./config.txt", "w")
            config.write(lizenz["lizenz"])
            config.close()

            new = lizenz["lizenz"]
            overwrite = True
        except:
            pass

    data = {
        "old": old,
        "new": new,
        "bool": overwrite
    }


    return data



# delay mithilfe einer Zufallsvariable um die Menge an eingehenden Requests zu verteilen (Load Performace)
zufall = random.uniform(10, 100)
time.sleep(zufall)

# Führt den Heartbeat-Request-Prozess aus
execute()



#Fürt die autostartlizenz.bat Datei aus um den Windows Task Scheduler zu registrieren (nur einmalig mithilfe des initial.txt)
firstTime = open("lizenzinitial.txt", "r").read()
firstTime.replace("\n", "")

if firstTime.lower() == "false":
    subprocess.call([r'.\autostartlizenz.bat'])
    open("lizenzinitial.txt", "w").write("True")
