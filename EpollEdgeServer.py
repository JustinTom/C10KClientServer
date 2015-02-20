'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    EpollEdgeServer.py - A simple echo server using the edge triggered interface of the epoll API
--
--  PROGRAM:        Epoll method server using epoll edge-triggered
--                  python epollEdgeServer.py
--
--  FUNCTIONS:      run(hostIP, port), close()
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
    serversocket.listen(0)
    #Since sockets are blocking by default, this is necessary to use non-blocking     (asynchronous) mode.
    serversocket.setblocking(0)
    #serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    epoll = select.epoll()
    #Register interest in read events on the server socket. A read event will occur     any time the server socket accepts a socket connection.
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

    try:
        #The connection dictionary maps file descriptors (integers) to their     corresponding network connection objects.
        connections = {}; requests = {}; responses = {}
        while running:
            events = epoll.poll(-1)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    clientConnection, clientAddress = serversocket.accept()
                    counter+=1
                    clientConnection.setblocking(0)
                    requests.update({clientConnection.fileno(): clientConnection})
                    epoll.register(clientConnection.fileno(), select.EPOLLIN | select.EPOLLET)
                    print (str(clientAddress) + " : " + " Just Connected. \n Currently connected clients: " + str(counter) + "\n")
                    text_file.write(str(clientAddress) + " : " + " Just Connected. \n Currently connected clients: " + str(counter) + "\n")

                elif event & select.EPOLLIN:
                    receiveSock = requests.get(fileno)
                    
                    try:
                        data = receiveSock.recv(bufferSize)
                        #timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                        dataSize = len(data)
                        dataTotal += dataSize
                        #text_file.write(str(timeStamp) + " - Size of data received (" + clientIP + ":" + str(clientSocket) + ") = " + str(dataSize) + '\n')
                        receiveSock.send(data)
                    except:
                        pass


                elif event & select.EPOLLERR:
                    counter-=1
                    
                elif event & select.EPOLLHUP:
                    counter-=1
                    
    except KeyboardInterrupt:
        print ("\nA keyboardInterruption has occured.")
        close(epoll, serversocket, counter, dataTotal)
    
    except Exception,e:
        print ("Unknown Error has occured." + str(e))
        close(epoll, serversocket, counter, dataTotal)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       close
--  Developer:  Kyle Gilles, Justin Tom
--  Created On: Feb. 10, 2015
--  Parameters:
--      none
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
 
    text_file = open(str(getTime()) + "_EpollEdgeServerLog.txt", "w")

    #Create and initialize the text file with the date in the filename in the logfiles directory
    #text_file = open("./Logfiles/" + str(getTime()) + "_SelectServerLog.txt", "w")
    
    run(hostIP, port)
               
