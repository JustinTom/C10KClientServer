'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    echoClient.py - A simple TCP client program.
--
--  PROGRAM:        Single threaded client
--                  python echoClient.py
--
--  FUNCTIONS:      run()
--
--  DATE:           February 10, 2015
--
--  REVISIONS:      February 18, 2015
--
--  DESIGNERS:      Kyle Gilles, Justin Tom
--
--  PROGRAMMERS:    Kyle Gilles, Justin Tom
--
--  NOTES:
--  The program will accept TCP connections from a user specified server and port.
--  The server will be specified by the IP address.
--  The user will be prompted for the data to send, how many clients to simulate 
--  and how many number of times each client will send that data.
--  The application will also keep a log file of the data sent and received as well as 
--  round trip times for each sent data and the average RTT of all the data sent
--  Test with accompanying server applications: multithreadServer.py, epollSelectServer.py and epollEdgeLevelServer.py
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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       run
--  Developer:  Kyle Gilles, Justin Tom
--  Created On: Feb. 10, 2015
--  Parameters:
--      clientNumber
--          the IP address of the host
--  Return Values:
--    none
--  Description:
--    Connects the socket to the specified server and port to both send
--    and receive the echoed data.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
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