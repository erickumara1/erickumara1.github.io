
import socket
import sys

host = "127.0.0.1"
port = 9999

def createSocket():
    try:
        global s
        s = socket.socket()  
    except socket.error as msg:
        print("Socket Creation Error: " + str(msg))

def bindSocket():
    try:
        global s
        print("Binding Port: " + str(port))

        s.bind((host, port)) 
        s.listen(5) 

    except socket.error as msg:
        print("Socket Binding Error: " + str(msg) + "\n" + "Retrying...")
        bindSocket() 

def acceptSocket():
    connection, address = s.accept()
    print("Connection Established With: IP " + address[0] + ", Port: " + str(address[1]))

    sendCommand(connection)

    connection.close()

def sendCommand(connection):
    while True:
        cmd = input()
        if cmd == "quit":
            connection.close()
            s.close()
            sys.exit()

        if len(str.encode(cmd)) > 0:
            connection.send(str.encode(cmd))
            clientResponse = str(connection.recv(1024), "utf-8")
            print(clientResponse, end="")

def main():
    createSocket()
    bindSocket()
    acceptSocket()

main()