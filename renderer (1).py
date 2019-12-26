#Michael Nguyen

#import modules
from socket import *
import select
import os
import sys

#Server Methods

chunkid = 1
pause = 1
filename = ""


def requestChunk(conSocket, fileName):
    response = ("PFCAFS 1.0 \r\nTARGET RESOURCE SERVER \r\nREQUEST CHUNK \r\n\r\n")
    global chunkid
    global filename
    filename = fileName

    response = response + fileName + "," + str(chunkid)
    chunkid = int(chunkid) + 1

    conSocket.send(response.encode())

    print("Chunk Request Sent")
    #sys.exit()

def renderChunk(conSocket, serverSocket, renderedFile):
    global pause
    response = ("PFCAFS 1.0 \r\nTARGET RESOURCE CONTROLLER \r\nRESPONSE TO START \r\n\r\n")

    response = response + renderedFile + " \r\n"

    conSocket.send(response.encode())
    print("Rendered Chunk Sent")
    # if(response.find('x00') == -1 and pause != 1):
    #     requestChunk(serverSocket, filename)

    if(response.find('x00') != -1):
        pause = 1


def requestPause():
    global pause
    pause =1

def requestResume():
    global pause
    pause =0

def requestRestart():
    global chunkid
    global pause
    chunkid = 1
    pause =0


#Server RUN

serverIP = str(sys.argv[1])
controllerSocket = socket(AF_INET, SOCK_STREAM)
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
controllerSocket.bind(('',9842))
controllerSocket.listen(0)

print ('Connecting to Server')
serverSocket.connect((serverIP, 9842))
print ('Server connected')

print ('Waiting on Controller')
conSocket, addr = controllerSocket.accept()
print ('Controller connected...')

sockets = [serverSocket, conSocket]

while True:

        print("Checking for Request")
        ready_sockets,_,_ = select.select(sockets,[], [], 2)

        print(len(ready_sockets))

        if len(ready_sockets) == 0:
            if pause == 0:
                requestChunk(serverSocket, filename)

        for socket in ready_sockets:
            message = socket.recv(1024)
            message = message.decode("utf-8")
            message = message.splitlines() #Split message into lines
            print(message)

            try:
                 assert(message[0] == "PFCAFS 1.0 ")

            except AssertionError:
                print("Given Protocol:")
                print(message[0])
                connectionSocket.send('Incorrect Protocol Specified'.encode())

            try:
                assert(message[1] == "TARGET RESOURCE RENDERER ")

            except AssertionError:
                print("Given target:")
                print(message[1])
                connectionSocket.send('Incorrect Target Specified'.encode())

            try:
                if(message[2] == "REQUEST START " ):
                    pause = 0
                    filename = message[4]
                    requestChunk(serverSocket, filename)
                elif(message[2] == "RESPONSE TO CHUNK "):
                    chunkMessage = message[4]
                    renderChunk(conSocket, serverSocket, chunkMessage)
                elif(message[2] == "REQUEST PAUSE "):
                    requestPause()
                elif(message[2] == "REQUEST RESUME "):
                    requestResume()
                    requestChunk(serverSocket,filename)
                elif(message[2] == "REQUEST RESTART "):
                    requestRestart()
                    requestChunk(serverSocket,filename)
                else:
                    raise AssertionError()

            except AssertionError:
                print("Given Command:")
                print(message[2])
                connectionSocket.send('Command name invalid'.encode())

        #connectionSocket.close()
