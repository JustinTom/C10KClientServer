from socket import *
import threading
import thread
import time
import datetime
 


def handler(clientsocket, clientaddr):
    global connections
    global con
    
    while 1:
       
        data = clientsocket.recv(1024)
        
        msg = "You sent me: %s" % data
        clientsocket.send(msg)
        


def counter():
    while 1: 
        #print ('active connections is: ' + str(len(connections)))
        print ('active connections is: ' + str(threading.activeCount()))
        t = (5)
        time.sleep(t)



 
if __name__ == "__main__":
    
    con = 0
    connections = []

    host = 'localhost'
    port = 55573
    buf = 1024
 
    addr = (host, port)
 
    serversocket = socket(AF_INET, SOCK_STREAM)
    CountThread = threading.Thread(target = counter)
    CountThread.start()
 
    serversocket.bind(addr)

 
    serversocket.listen(1)
    print "Server is listening for connections\n"
    

    

    while 1:
       

        


        clientsocket, clientaddr = serversocket.accept()

        thread.start_new_thread(handler, (clientsocket, clientaddr))
        connections.append(thread)
    serversocket.close()