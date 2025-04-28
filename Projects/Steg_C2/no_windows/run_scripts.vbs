Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw sunshine.py", 0, False
WScript.Sleep 5000 
WshShell.Run "pythonw sunfire.py", 0, False
WScript.Sleep 5000 
WshShell.Run "pythonw client.py", 0, False