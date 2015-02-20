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
 


def handler(clientsocket, clientaddr):
    global dataTotal
    while 1:
        
        data = clientsocket.recv(bufferSize)
        dataSize = len(data)
        dataTotal += dataSize
        clientsocket.send(data)
        

def close():
    print ("Closing the server...")
    text_file.write("\n\nTotal number of connections: " + str(counter))
    text_file.write("\nTotal amount of data transferred: " + str(dataTotal))
    text_file.close()
    sys.exit()
          


if __name__ == '__main__':
    hostIP = raw_input('Enter your host IP \n')
    port = int(input('What port would you like to use?\n'))
    connections = []
    counter = 0
    dataTotal = 0
    bufferSize = 1024
    #dataTotal = 0
    ts = time.time()
    con = 0
    
    curTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H.%M.%S')

    text_file = open(curTime + "_ThreadedServerLog.txt", "w")
    
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
            text_file.write(str(clientaddr) + " : " + " Just Connected. \n Currently connected clients: " + str(counter) + "\n")
            clientThread = threading.Thread(target = handler, args=(clientsocket, clientaddr))
            clientThread.start()
    
    except KeyboardInterrupt:
        print ("A keyboardInterruption has occured.")
        close()
        
        
    
    except Exception,e:
        print ("Unknown Error has occured." + str(e))
        close()
        
        
    
   

    

    

    
