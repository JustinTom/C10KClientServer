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
serversocket.listen(0)
#Since sockets are blocking by default, this is necessary to use non-blocking (asynchronous) mode.
serversocket.setblocking(0)
#serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

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
            
                
           
	
            #If a write event occurred on a client socket, it's able to accept new data to send to the client.
            
#Open socket connections don't need to be closed since Python will close them when the program terminates. They're included as a matter of good form.
finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()
