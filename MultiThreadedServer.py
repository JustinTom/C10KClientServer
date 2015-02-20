'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    MultiThreadedServer.py - A simple echo server using the edge triggered interface of the epoll API
--
--  PROGRAM:        Select method server using epoll edge-triggered
--                  python epollSelectServer.py
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
import threading
import thread
import time
import datetime
import sys

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       threadHandler
--  Developer:  Kyle Gilles
--  Created On: Feb. 18, 2015
--  Parameters:
--      clientsocket
--          Required to pass the variable to the next function    
--      clientaddr
--          Address of the client thread has connection with            
--  Return Values:
--     none
--  Description:
--    When a client establishes a connection a thread is created and this is its loop.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  

def threadHandler(clientsocket, clientaddr):
    global dataReceivedTotal
    global dataSentTotal
    while 1:
        
        data = clientsocket.recv(bufferSize)
        clientIP, clientSocket = clientsocket.getpeername()
        dataRSize = len(data)
        dataReceivedTotal += dataRSize
        text_file.write(str(getTime()) + " - Size of data received (" + clientIP + ":" + str(clientSocket) + ") = " + str(dataRSize) + '\n')
        clientsocket.send(data)
        dataSSize = len(data)
        dataSentTotal += dataSSize
        text_file.write(str(getTime()) + " - Size of data sent (" + clientIP + ":" + str(clientSocket) + ") = " + str(dataSSize) + '\n')
        
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
def close():
    print ("Closing the server...")
    text_file.write("\n\nTotal number of connections: " + str(counter))
    text_file.write("\nTotal amount of data received: " + str(dataReceivedTotal))
    text_file.write("\nTotal amount of data sent: " + str(dataSentTotal))
    text_file.close()
    sys.exit()
          
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
    connections = []
    counter = 0
    dataTotal = 0
    bufferSize = 1024
    
    #Create and initialize the text file with the date in the filename in the logfiles directory   
    text_file = open("./Logfiles/" + str(getTime()) + "_MultiThreadedServerLog.txt", "w")

    addr = (hostIP, port)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(addr)
    serversocket.listen(50)
    print ("Server is listening for connections\n")

    
    try: 
        while 1: 
            clientsocket, clientaddr = serversocket.accept()
            counter += 1
            print (str(clientaddr) + " : " + " Just Connected. \n Currently connected clients: " + str(counter) + "\n")
            text_file.write(str(getTime()) + " - " str(clientaddr) + " : " + " Just Connected. \n Currently connected clients: " + str(counter) + "\n")
            clientThread = threading.Thread(target = threadHandler, args=(clientsocket, clientaddr))
            clientThread.start()
    
    except KeyboardInterrupt:
        print ("A keyboardInterruption has occured.")
        close()
        
        
    
    except Exception,e:
        print ("Unknown Error has occured." + str(e))
        close()
        
        
    
   

    

    

    
