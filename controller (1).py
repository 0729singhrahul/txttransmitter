#Daniel Mains

#import modules
from socket import *
import os
import sys
import select

def requestList(clientSocketServer):
    clientSocketServer.send('PFCAFS 1.0 \r\nTARGET RESOURCE SERVER \r\nREQUEST LIST \r\n\r\n'.encode())

def startRender(clientSocketRenderer, filename):
    message = 'PFCAFS 1.0 \r\nTARGET RESOURCE RENDERER \r\nREQUEST START \r\n\r\n' + filename + '\r\n'
    clientSocketRenderer.send(message.encode())

def pauseRender(clientSocketRenderer):
    message = 'PFCAFS 1.0 \r\nTARGET RESOURCE RENDERER \r\nREQUEST PAUSE \r\n\r\n'
    clientSocketRenderer.send(message.encode())

def resumeRender(clientSocketRenderer):
    message = 'PFCAFS 1.0 \r\nTARGET RESOURCE RENDERER \r\nREQUEST RESUME \r\n\r\n'
    clientSocketRenderer.send(message.encode())

def restartRender(clientSocketRenderer):
    message = 'PFCAFS 1.0 \r\nTARGET RESOURCE RENDERER \r\nREQUEST RESTART \r\n\r\n'
    clientSocketRenderer.send(message.encode())

def displayRender(message):
    print(message[4][1:] + "\n")


#Setup Socket connections
clientSocketServer = socket(AF_INET, SOCK_STREAM)
clientSocketRenderer = socket(AF_INET, SOCK_STREAM)

serverIP = str(sys.argv[1])
rendererIP = str(sys.argv[2])

clientSocketServer.connect((serverIP, 9842))
print("Connected to Server...\n")
clientSocketRenderer.connect((rendererIP, 9842))
print("Connected to Renderer...\n")

""" MAIN """

requestList(clientSocketServer)
message = clientSocketServer.recv(1028)

print(message.decode("utf-8"))

filename = input("Choose a file...\n")
print("Input Commands to control file stream: (Start, Pause, Resume, Restart)\n")

while True:

    ready_inputs,_,_ = select.select([sys.stdin], [], [], 2)

    for input in ready_inputs:
        command = sys.stdin.readline().strip()
        #print(command)

        if(command == "Start"):
            startRender(clientSocketRenderer, filename)
        elif(command == "Pause"):
            pauseRender(clientSocketRenderer)
        elif(command == "Resume"):
            resumeRender(clientSocketRenderer)
        elif(command == "Restart"):
            restartRender(clientSocketRenderer)
        elif(command == "Exit"):
            print("Thank you for using our application.")
            sys.exit()
        else:
            print("Invalid Command")

    ready_sockets,_,_ = select.select([clientSocketRenderer],[], [], .5)

    for socket in ready_sockets:
        message = socket.recv(1024)
        message = message.decode("utf-8")
        message = message.splitlines() #Split message into lines

        if(message[2] == "RESPONSE TO START "):
            displayRender(message)

    # command = input("Input Command (Start, Pause, Resume, Restart)\n")
