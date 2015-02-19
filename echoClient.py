'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:        epoll_svr.c -   A simple echo server using the epoll API
--
--  PROGRAM:        epolls
--              gcc -Wall -ggdb -o epolls epoll_svr.c  
--
--  FUNCTIONS:      close
--
--  DATE:           February 10, 2015
--
--  REVISIONS:      February 18, 2015
--
--  DESIGNERS:      Kyle Gilles, Justin Tom
--
--  PROGRAMMERS:    Justin Tom, Kyle Gilles
--
--  NOTES:
--  The program will accept TCP connections from client machines.
--  The program will read data from the client socket and simply echo it back.
--  Design is a simple, single-threaded server using non-blocking, edge-triggered
--  I/O to handle simultaneous inbound connections. 
--  Test with accompanying client application: epoll_clnt.c
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python

from socket import *
import threading
import time
import random
import sys

host = raw_input('Enter the server IP: ')
port = int(input('Enter the port: '))
clients = int(input('Enter number of clients: '))
message = raw_input('Enter a message to send: ')
msgMultiple = int(input('Enter the number of times you would like to send the message: '))


def run (clientNumber):
    buf = 1024

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host,port))

    while 1:
        for _ in range( msgMultiple ):
            #cData = message + str(clientNumber)
            cData = message
            start = time.time()
            s.send(cData.encode('utf-8'))
            print "Sent: " + cData
            sData = s.recv(buf)
            end =  time.time()
            response_time = end - start
            totalTime += response_time
            print "Received: " + cData + '\n'
            t = random.randint(0, 9)
            time.sleep(t)

if __name__ == '__main__':
    threads = []
    totalTime = 0
    for x in range ( clients ):
    
        thread = threading.Thread(target = run, args = [x])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    bytes = sys.getsizeof(message)
    totalRequests = clients * numberOfMessages
    totalBytes = totalRequests * bytes
    averageRTT = totalTime / totalRequests
    print("Bytes sent in message was : " + str(bytes))
    print("Total Data sent was : " + str(totalBytes) + " Bytes." )
    print("Average RTT was : " + str (averageRTT) + " seconds." )
    print("Requests was : " + str (totalRequests))