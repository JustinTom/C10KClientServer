'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    epollSelectServer.py - A simple echo server using the level triggered interface of the epoll API
--
--  PROGRAM:        Select method server using epoll
--                  python epollSelectServer.py
--
--  FUNCTIONS:      run(hostIP, port), close(epoll, serversocket, counter, dataTotal), getTime()
--
--  DATE:           February 10, 2015
--
--  REVISIONS:      February 18, 2015
--
--  DESIGNERS:      Justin Tom
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
import datetime
import time
import logging

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       run
--  Developer:  Kyle Gilles, Justin Tom
--  Created On: Feb. 10, 2015
--  Parameters:
--      hostIP
--          the IP address of the host
--      port
--          the port to listen on
--  Return Values:
--      none
--  Description:
--      Listens on the specified socket for incoming data, sets a counter for connected clientSocket
--      and echoes back the received data.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def run(hostIP, port):
    running = 1
    counter = 0
    bufferSize = 1024
    dataSentTotal = 0
    dataReceivedTotal = 0
    dataSSize = 0
    dataRSize = 0
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((hostIP, port))
    #The listen backlog queue size
    serversocket.listen(socket.SOMAXCONN)
    #Since sockets are blocking by default, this is necessary to use non-blocking (asynchronous) mode.
    serversocket.setblocking(0)
    #Create an epoll object.
    epoll = select.epoll()
    #Register interest in read events on the server socket. A read event will occur any time the server socket accepts a socket connection.
    epoll.register(serversocket.fileno(), select.EPOLLIN)
    try:
        #The connection dictionary maps file descriptors (integers) to their corresponding network connection objects.
        requests = {}
        while running:
            #Query the epoll object to find out if any events of interest may have occurred. The parameter "1" signifies that we are willing to wait up to one second for such an event to occur. If any events of interest occurred prior to this query, the query will return immediately with a list of those events.
            events = epoll.poll(-1)
            #Events are returned as a sequence of (fileno, event code) tuples. fileno is a synonym for file descriptor and is always an integer.
            for fileno, event in events:
                #If a read event occurred on the socket server, then a new socket connection may have been created.
                if fileno == serversocket.fileno():
                    clientConnection, clientAddress = serversocket.accept()
                    counter+=1
                    requests.update({clientConnection.fileno(): clientConnection})
                    #Set new socket to non-blocking mode.
                    clientConnection.setblocking(0)
                    #Register interest in read (EPOLLIN) events for the new socket.
                    epoll.register(clientConnection.fileno(), select.EPOLLIN)
                    logging.info(str(clientAddress) + " just connected.")
                    logging.info("Currently connected clients: " + str(counter))
                    print (str(clientAddress) + " just connected. \nCurrently connected clients: " + str(counter))
                elif event & select.EPOLLIN:
                    receiveSock = requests.get(fileno)
                    data = receiveSock.recv(bufferSize)
                    clientIP, clientSocket = receiveSock.getpeername()
                    dataRSize = len(data)
                    dataReceivedTotal += dataRSize
                    logging.info("Size of data received (" + clientIP + ":" + str(clientSocket) + ") = " + str(dataRSize))
                    dataSSize = len(data)
                    dataSentTotal += dataSSize
                    receiveSock.send(data)
                    logging.info("Size of data sent (" + clientIP + ":" + str(clientSocket) + ") = " + str(dataSSize))
                elif event & select.EPOLLERR:
                    counter-=1
                elif event & select.EPOLLHUP:
                    counter-=1
    #Handle keyboard interrupts (Mainly ctrl+c)
    except KeyboardInterrupt:
        close(epoll, serversocket, counter, dataReceivedTotal, dataSentTotal)
        print ("\nA keyboardInterruption has occured.")
    #Handle all other exceptions in hopes to close 'cleanly'
    except Exception,e:
        print ("Server connection has ran into an unexpected error: " + str(e))
        close(epoll, serversocket, counter, dataReceivedTotal, dataSentTotal) 

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       close
--  Developer:  Kyle Gilles, Justin Tom
--  Created On: Feb. 10, 2015
--  Parameters:
--      epoll
--          Epoll object required to close and clean up
--      serversocket
--          Server socket object required to close it
--      counter
--          Counter for total amount of connections.
--      dataReceivedTotal
--          Total number of data bytes received from the client to the server
--      dataSentTotal
--          Total number of data bytes sent to the client from server
--  Return Values:
--      none
--  Description:
--    Cleans up and closes the epoll objects, and sockets as well as closing the log text file.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def close(epoll, serversocket, counter, dataReceivedTotal, dataSentTotal):
    epoll.unregister(serversocket.fileno())
    epoll.close()
    print ("\nClosing the server...")
    serversocket.close()

    logging.info("\n\nTotal number of connections: " + str(counter))
    logging.info("Total amount of data received: " + str(dataReceivedTotal))
    logging.info("Total amount of data sent: " + str(dataSentTotal))

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

if __name__ == '__main__':
    hostIP = raw_input('Enter your host IP \n')
    port = int(input('What port would you like to use?\n'))

    logging.basicConfig(filename='./Logfiles/' + str(getTime()) + '_SelectServerLog.txt', 
                        filemode='w', 
                        level=logging.INFO, 
                        format='%(asctime)s - %(message)s', 
                        datefmt='%H:%M:%S')

    run(hostIP, port)
