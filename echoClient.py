#!/usr/bin/env python 

""" 
A simple echo client 
""" 

from socket import *
import threading
import time
import random




port = int(input('Enter the port: '))
host = raw_input('Enter the server IP: ')
clients = int(input('Enter number of clients: '))
message = raw_input('Enter a message to send: ')
msgMultiple = int(input('Enter the number of times you would like to send the message: '))
buf = 1024






def run (clientNumber):
    s = socket(AF_INET, SOCK_STREAM)

    s.connect((host,port))

    while 1:
        for _ in range( msgMultiple ):
            #cData = message + str(clientNumber)
            cData = message
            s.send(cData.encode('utf-8'))
            print "Sent: " + cData
            sData = s.recv(buf)
            print "Received: " + cData + '\n'
            t = random.randint(0, 9)
            time.sleep(t)


if __name__ == '__main__':
    threads = []
    for x in range ( clients ):
    
        thread = threading.Thread(target = run, args = [x])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()






