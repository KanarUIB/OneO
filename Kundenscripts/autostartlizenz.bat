@echo off

start cmd /c SCHTASKS /CREATE /TN "LizenzUpdate" /TR ".\lizenz.exe" /ST 11:00 /SC MONTHLY /MO 3
