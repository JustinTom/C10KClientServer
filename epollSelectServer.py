'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    epollSelectServer.py - A simple echo server using the edge triggered interface of the epoll API
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
--  Design is a simple, single-threaded server using non-blocking, edge-triggered
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
    dataTotal = 0
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((hostIP, port))
    #The listen backlog queue size
    serversocket.listen(10000)
    #Since sockets are blocking by default, this is necessary to use non-blocking (asynchronous) mode.
    serversocket.setblocking(0)
    #Create an epoll object.
    epoll = select.epoll()
    #Register interest in read events on the server socket. A read event will occur any time the server socket accepts a socket connection.
    epoll.register(serversocket.fileno(), select.EPOLLIN)
    try:
        #The connection dictionary maps file descriptors (integers) to their corresponding network connection objects.
        connections = {}; requests = {}; responses = {}
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
                    #Connected clients print moved to after register due to multiple prints showing same number
                    text_file.write(str(getTime()) + "Currently connected clients: " + str(counter) + '\n')
                    print 'Currently connected clients: ' + str(counter)
                elif event & select.EPOLLIN:
                    receiveSock = requests.get(fileno)
                    data = receiveSock.recv(bufferSize)
                    clientIP, clientSocket = receiveSock.getpeername()
                    #print 'Currently connected clients: ' + str(counter)
                    dataSize = len(data)
                    dataTotal += dataSize
                    text_file.write(str(getTime()) + " - Size of data received (" + clientIP + ":" + str(clientSocket) + ") = " + str(dataSize) + '\n')
                    #print 'Data(' + clientIP + ':' + str(clientSocket) + ') = ' + data + '\n'
                    receiveSock.send(data)
                elif event & select.EPOLLERR:
                    counter-=1
                elif event & select.EPOLLHUP:
                    counter-=1
    except KeyboardInterrupt:
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
    return

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

    #Create and initialize the text file with the date in the filename
    text_file = open(str(getTime()) + "_SelectServerLog.txt", "w")

    run(hostIP, port)
