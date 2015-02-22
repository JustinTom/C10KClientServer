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
--  The program is built for performance and does not log or output anything.
--  Test with accompanying client application: echoClient.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python
import socket
import threading
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
    global dataTotal
    while 1:
        data = clientsocket.recv(bufferSize)
        clientsocket.send(data)
        
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
--  Return Values:
--      none
--  Description:
--    Cleans up and closes the epoll objects, and sockets as well as closing the log text file.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def close():
    print ("Closing the server...")
    sys.exit()


if __name__ == '__main__':
    hostIP = raw_input('Enter your host IP \n')
    port = int(input('What port would you like to use?\n'))
    #Maintain how many connections
    connections = []
    bufferSize = 1024
    addr = (hostIP, port)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Bind server to port
    serversocket.bind(addr)
    #The listen backlog queue size
    serversocket.listen(50)
    
    try: 
        while 1: 
            #Accept client connections
            clientsocket, clientaddr = serversocket.accept()
            #Create a thread for each client connection
            clientThread = threading.Thread(target = threadHandler, args=(clientsocket, clientaddr))
            clientThread.start()
    
    except KeyboardInterrupt:
        print ("A keyboardInterruption has occured.")
        close()       
    
    except Exception,e:
        print ("Unknown Error has occured." + str(e))
        close()
        
        
    
   

    

    

    
