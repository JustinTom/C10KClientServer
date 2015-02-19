import socket
import select
import thread
import threading


def threadFunc():
    global requests
    
    global counter
    global epoll
    global running
    global buffersize
    global serversocket
    

    #The connection dictionary maps file descriptors (integers) to their corresponding network connection objects.
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
                clientConnection = requests.get(fileno)
 
		try:
                    data = receiveSock.recv(bufferSize)
                    if data!=0:
                        
                        #
                        #print 'Data: ' + data
                        receiveSock.send(data)
		except:
                    counter-= 1
                    pass
	"""
            elif event & select.EPOLLERR:
                counter-=1
            elif event & select.EPOLLHUP:
                counter-=1

finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()
"""


    

if __name__=="__main__":

    hostIP = raw_input('Enter your host IP \n')
    port = int(input('What port would you like to use?\n'))
    requests = {}
    running = 1
    bufferSize = 1024
    counter = 0
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((hostIP, port))
    serversocket.listen(0)
    serversocket.setblocking(0)
    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)
    requests.update({serversocket.fileno(): serversocket})
    
    for x in range(0, 3):
        sThread = threading.Thread(target = threadFunc)
        sThread.start()
