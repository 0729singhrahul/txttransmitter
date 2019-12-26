#Daniel Mains

#import modules
from socket import *
import os
import sys

#Server Methods

def sendList(connectionSocket):
    response = ("PFCAFS 1.0 \r\nTARGET RESOURCE CONTROLLER \r\nRESPONSE TO LIST \r\n\r\n")

    for file in os.listdir():
        if(file.endswith(".py")):
            continue
        response = response + file + "," + str(os.stat(file).st_size) + "\r\n"

    connectionSocket.send(response.encode())

    print("File list sent")
    #sys.exit()

def sendChunk(connectionSocket, chunkInfo):
    chunkInfo = chunkInfo.split(",")
    #print(chunkInfo)
    filename = chunkInfo[0]
    chunkID = int(chunkInfo[1])

    f = open(filename)
    f.seek(100*(chunkID-1))
    outputChunk = f.read(100)

    outputChunk = outputChunk.encode()
    if(sys.getsizeof(outputChunk) < 100):
        outputChunk = outputChunk + bytes(100-sys.getsizeof(outputChunk))

    response = ("PFCAFS 1.0 \r\nTARGET RESOURCE RENDERER \r\nRESPONSE TO CHUNK \r\n\r\n")
    response = response + str(outputChunk) + " \r\n"

    connectionSocket.send(response.encode())

    print("Chunk " + str(chunkID) + " from file: " + filename + " sent.")
    #sys.exit()

#Server RUN

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind(('',9842))
serverSocket.listen(5)

print ('Waiting for Renderer')
rendererSocket, addr = serverSocket.accept()
print ('Renderer connected')

print ('Waiting for Controller')
controllerSocket, addr = serverSocket.accept()
print ('Controller connected')

print ('Waiting for File Request')
message = controllerSocket.recv(1024) #Fill in start #Fill in end
message = message.decode("utf-8")
message = message.splitlines() #Split message into lines
try:
    if(message[2] == "REQUEST LIST "):
        sendList(controllerSocket)
    else:
        raise AssertionError()
except AssertionError:
    print("Given Command:")
    print(message[2])
    connectionSocket.send('Please send a file request'.encode())


while True:
        #Establish the connection
        print('Waiting for Renderer')
        message = rendererSocket.recv(1024)
        message = message.decode("utf-8")
        message = message.splitlines() #Split message into lines

        try:
             assert(message[0] == "PFCAFS 1.0 ")

        except AssertionError:
            print("Given Protocol:")
            print(message[0])
            rendererSocket.send('Incorrect Protocol Specified'.encode())

        try:
            assert(message[1] == "TARGET RESOURCE SERVER ")

        except AssertionError:
            print("Given target:")
            print(message[1])
            rendererSocket.send('Incorrect Target Specified'.encode())

        try:
            if(message[2] == "REQUEST CHUNK "):
                chunkInfo = message[4]
                sendChunk(rendererSocket, chunkInfo)
            else:
                raise AssertionError()

        except AssertionError:
            print("Given Command:")
            print(message[2])
            rendererSocket.send('Command name invalid'.encode())

        #connectionSocket.close()
