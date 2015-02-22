'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    EpollEdgeServer-Testing.py - A simple echo server using the edge triggered interface of the epoll API
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
--  This program is built for performance and does not output clients connected or log information such as amount of data transferred.
--  Test with accompanying client application: echoClient.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import socket
import select
import thread


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
    bufferSize = 1024
    #Create an epoll object
    epoll = select.epoll()
    #The connection dictionary maps file descriptors (integers) to their corresponding network connection objects.
    requests = {}
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Register interest in read events on the server socket. A read event will occur any time the server socket accepts a socket connection.
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)
    #Add server filno to array
    requests.update({serversocket.fileno(): serversocket})
    #This method allows a bind() to occur even if a program was recently bound to the port.
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((hostIP, port))
    #The listen backlog queue size
    serversocket.listen(10000)
    #Since sockets are blocking by default, this is necessary to use non-blocking (asynchronous) mode.
    serversocket.setblocking(0)

    
    
    try:
        
        while running:
            events = epoll.poll(-1)
            for fileno, event in events:
                # If a socket connection has been created
                if fileno == serversocket.fileno(): 
                    clientConnection, clientAddress = serversocket.accept()
                    #Set client connection to non blocking
                    clientConnection.setblocking(0)
                    requests.update({clientConnection.fileno(): clientConnection})
                    #Register EPOLLIN interest.
                    epoll.register(clientConnection.fileno(), select.EPOLLIN | select.EPOLLET)
                
                #If a read event occured, get client data
                elif event & select.EPOLLIN:
                    clientConnection = requests.get(fileno)
                    # Send client data back 
                    try:
                        data = clientConnection.recv(bufferSize)
                        clientConnection.send(data)
		    except:
                        pass

    # Handle a keyboard disconnect.
    except KeyboardInterrupt:
        print ("\nA keyboardInterruption has occured.")
        close(epoll, serversocket)
    
    #except Exception,e:
        #print ("Unknown Error has occured." + str(e))
        #close(epoll, serversocket)

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
                
def close(epoll, serversocket):
    epoll.unregister(serversocket.fileno())
    epoll.close()
    print("\nClosing the server...")
    serversocket.close()            
	
 
if __name__=='__main__':
    
    hostIP = raw_input('Enter your host IP \n')
    port = int(input('What port would you like to use?\n'))
    run(hostIP, port)
