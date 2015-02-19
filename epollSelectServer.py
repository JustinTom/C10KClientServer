import socket
import select
import thread

hostIP = raw_input('Enter your host IP \n')
port = int(input('What port would you like to use?\n'))

running = 1
bufferSize = 1024
counter = 0
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((hostIP, port))
#The listen backlog queue size
serversocket.listen(50)
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
            elif event & select.EPOLLIN:
                receiveSock = requests.get(fileno)
                data = receiveSock.recv(bufferSize)
                clientIP, clientSocket = receiveSock.getpeername()
            	print 'Currently connected clients: ' + str(counter) + '\n'
                print 'Data (' + clientIP + ':' + str(clientSocket) + ') = ' + data + '\n'
                receiveSock.send(data)
            elif event & select.EPOLLERR:
                counter-=1
            elif event & select.EPOLLHUP:
                counter-=1
#Open socket connections don't need to be closed since Python will close them when the program terminates. They're included as a matter of good form.
finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()
