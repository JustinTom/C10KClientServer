'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    epollEdgeLevelSelect.py - A multi-threaded echo server using the level triggered interface of the epoll API
--
--  PROGRAM:        Select method server using epoll
--                  python epollSelectServer.py
--
--  FUNCTIONS:      threadFunc()
--
--  DATE:           February 10, 2015
--
--  REVISIONS:      February 18, 2015
--
--  DESIGNERS:      Kyle Gilles
--
--  PROGRAMMERS:    Kyle Gilles, Justin Tom
--
--  NOTES:
--  The program will accept TCP connections from client machines.
--  The program will read data from the client socket and simply echo it back.
--  Design is a simple, single-threaded server using non-blocking, level-triggered
--  I/O to handle simultaneous inbound connections. 
--  The program will also keep a log file of the number of connections and all data being echoed.
--  Test with accompanying client application: echoClient.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python

import socket
import select
import thread
import threading
import datetime
import time

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       threadFunc
--  Developer:  Kyle Gilles, Justin Tom
--  Created On: Feb. 10, 2015
--  Parameters:
--      none
--  Return Values:
--      none
--  Description:
--      Listens on the specified socket for incoming data, sets a counter for connected clientSocket
--      and echoes back the received data.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def threadFunc():
    global requests
    global counter
    global epoll
    global running
    global buffersize
    global serversocket
    
    try:
        while running:
            events = epoll.poll(-1)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    clientConnection, clientAddress = serversocket.accept()
                    counter+=1
                    clientConnection.setblocking(0)
                    requests.update({clientConnection.fileno(): clientConnection})
                    epoll.register(clientConnection.fileno(), select.EPOLLIN | select.EPOLLET)
                    text_file.write(str(getTime()) + " - " + clientAddress + " just connected. \nCurrently connected clients: " + str(counter) + '\n')
                    print (clientAddress + " just connected. \nCurrently connected clients: " + str(counter))
                elif event & select.EPOLLIN:
                    receiveSock = requests.get(fileno)
                    clientConnection = requests.get(fileno)
                    clientIP, clientSocket = receiveSock.getpeername()
                    dataSize = len(data)
                    dataTotal += dataSize
                    text_file.write(str(getTime()) + " - Size of data received (" + clientIP + ":" + str(clientSocket) + ") = " + str(dataSize) + '\n')
                    data = receiveSock.recv(bufferSize)
                    receiveSock.send(data)
                elif event & select.EPOLLERR:
                    counter-=1
                elif event & select.EPOLLHUP:
                    counter-=1
    #Handle keyboard interrupts (Mainly ctrl+c)
    except KeyboardInterrupt:
        close(epoll, serversocket, counter, dataTotal)
    #Handle all other exceptions in hopes to close cleanly
    except:
        close(epoll, serversocket, counter, dataTotal) 

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       close
--  Developer:  Kyle Gilles, Justin Tom
--  Created On: Feb. 10, 2015
--  Parameters:
--      epoll
--          Required to pass the variable to the next function
--      serversocket
--          Required to pass the variable to the next function
--      counter
--          Required to pass the variable to the next function
--      dataTotal  
--          Required to pass the variable to the next function
--  Return Values:
--      none
--  Description:
--    Cleans up and closes the epoll objects, and sockets as well as closing the log text file.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def close(epoll, serversocket, counter, dataTotal):
    epoll.unregister(serversocket.fileno())
    epoll.close()
    print ("\nClosing the server...")
    serversocket.close()
    text_file.write("\n\nTotal number of connections: " + str(counter))
    text_file.write("\nTotal amount of data transferred: " + str(dataTotal))
    text_file.close()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       getTime
--  Developer:  Justin Tom
--  Created On: Feb. 18, 2015
--  Parameters:
--      none
--  Return Values:
--      timeStamp
--          The current time of when the function was called
--  Description:
--    Returns the current time of when the function was called in a Y-M-D H:M:S format
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp

if __name__=="__main__":
    hostIP = raw_input('Enter your host IP \n')
    port = int(input('What port would you like to use?\n'))
    log = raw_input('Would you like to keep a log of the server connections? (y/n)')

    #Create and initialize the text file with the date in the filename
    text_file = open("./Logfiles/" + str(getTime()) + "_EpollServerLog.txt", "w")

    requests = {}
    running = 1
    bufferSize = 1024
    counter = 0
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((hostIP, port))
    serversocket.listen(0)
    serversocket.setblocking(0)
    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)
    requests.update({serversocket.fileno(): serversocket})
    
    for x in range(0, 3):
        sThread = threading.Thread(target = threadFunc)
        sThread.start()
