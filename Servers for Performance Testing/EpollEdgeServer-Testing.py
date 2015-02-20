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
--  Test with accompanying client application: echoClient.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import socket
import select
import thread

def run(hostIP, port):
    running = 1
    bufferSize = 1024
    counter = 0
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((hostIP, port))
    #The listen backlog queue size
    serversocket.listen(0)
    #Since sockets are blocking by default, this is necessary to use non-blocking (asynchronous) mode.
    serversocket.setblocking(0)
    #Create an epoll object.
    epoll = select.epoll()
    #Register interest in read events on the server socket. A read event will occur any time the server socket accepts a socket connection.
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

    try:
        #The connection dictionary maps file descriptors (integers) to their corresponding network connection objects.
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
                    print 'Currently connected clients: ' + str(counter)


                elif event & select.EPOLLIN:
                    receiveSock = requests.get(fileno)
                
		    try:
                        data = receiveSock.recv(bufferSize)
                        receiveSock.send(data)
		    except:
                        pass
            
                
def close(epoll, serversocket):
    epoll.unregister(serversocket.fileno())
    epoll.close()
    print("\nClosing the server...")
    serversocket.close()            
	
 


if __name__=='__main__':
    
    hostIP = raw_input('Enter your host IP \n')
    port = int(input('What port would you like to use?\n'))
    run(hostIP, port)
