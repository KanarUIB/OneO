import requests
import os
import re


#logfile = open("D:/Development/Django/LOG.txt")

#logfile = open("C:/Users/Administrator/Desktop/ADDS/LOG.txt")

#log = print(" ".join(logfile.readlines()))
#print(re.split("[\s]",logfile.readlines()))


# REST API Schnittstelle
URL = "http://localhost:8000/heartbeat"

# Temporäre Localhostfreigabe für externe Clients
#URL = "https://e1715b876272.ngrok.io/heartbeat"

# Informationen zu Lizenzschluessel
lizenzschluessel = "APSDASDQ123123ASDLKA1231"

# Alle Parameter die mitgesendet werden:
# Lizenzschluessel sowie Errorlogs aus dem LOG File (falls Probleme bei der Kundensoftware registriert werden)
PARAMS = {'lizenzschluessel': lizenzschluessel, "meldung": "Test"}

# Post Request wird an API gesendet, mit jeweiligen Daten und dem URL Pfad
r = requests.post(url=URL, data=PARAMS)
