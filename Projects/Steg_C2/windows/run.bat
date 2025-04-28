@echo off
start /b python sunshine.py
timeout /t 15 /nobreak > nul
start /b python sunfire.py
timeout /t 10 /nobreak > nul
start /b python client.py
exit