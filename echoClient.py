#!/usr/bin/env python 

""" 
A simple echo client 
""" 

from socket import *
import threading
import time
import random





clients = int(input('Enter number of clients: '))
message = raw_input('Enter a message to send: ')
port = int(input('Enter the port: '))
host = raw_input('Enter the server IP: ')
#host = '192.168.0.23'





def run (clientNumber):
    global host
    #port = 55573
    buf = 1024
    global host
    global message


    s = socket(AF_INET, SOCK_STREAM)

    s.connect((host,port))

    while 1:
        cData = message + str(clientNumber)
        s.send(cData.encode('utf-8'))
        print "Sent: " + data + '\n'
        sData = s.recv(buf)
        print "Received: " + data + '\n'
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






