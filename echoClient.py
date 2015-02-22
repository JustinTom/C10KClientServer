'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    echoClient.py - A simple TCP client program.
--
--  PROGRAM:        Multi threaded client
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
import logging
import datetime

host = ""
port = 8005
message = ""
msgMultiple = 1


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
    global totalTime
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host,port))
    threadRTT = 0

    while 1:
        for _ in range( msgMultiple ):
            
            cData = message + "  From: Client " + str(clientNumber)
            #Start timer and send data
            start = time.time()
            s.send(cData.encode('utf-8'))
            print "Sent: " + cData
            #Stop timer when data is received
            sData = s.recv(buf)
            end =  time.time()
            #Keep track of RTT and update total time 
            response_time = end - start
            threadRTT += end - start
            totalTime += response_time
            print "Received: " + cData + '\n'
            t = random.randint(0, 9)
            time.sleep(t)
        #Log information of Client
        text_file.write("\nClient " + str(clientNumber) + " RTT time taken for " + str(msgMultiple) + " messages was: " + str(threadRTT) + " seconds.")
        threadRTT = 0
        break


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       getTime
--  Developer:  Justin Tom
--  Created On: Feb. 18, 2015
--  Parameters:
--      none
--  Return Values:
--      timeStamp
--          The current time of when the function was called
--  Description:
--    Returns the current time of when the function was called in a Y-M-D H:M:S format
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp     





    
if __name__ == '__main__': 
    host = raw_input('Enter the server IP: ')
    port = int(input('Enter the port: '))
    clients = int(input('Enter number of clients: '))
    message = raw_input('Enter a message to send: ')
    msgMultiple = int(input('Enter the number of times you would like to send the message: '))
    #Initialize Log file
    text_file = open("./Logfiles/" + str(getTime()) + "_ClientLog.txt", "w")
    #Used to maintain list of all running threads
    threads = []
    totalTime = 0
    
    #Create a seperate thread for each client
    for x in range ( clients ):
    
        thread = threading.Thread(target = run, args = [x])
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    #Calculations for log data
    bytes = sys.getsizeof(message)
    totalRequests = clients * msgMultiple
    totalBytes = totalRequests * bytes
    averageRTT = totalTime / totalRequests
    #Output data
    print("Bytes sent in message was : " + str(bytes))
    print("Total Data sent was : " + str(totalBytes) + " Bytes." )
    print("Average RTT was : " + str (averageRTT) + " seconds." )
    print("Requests was : " + str (totalRequests))
    #Write data to log file
    text_file.write("\n\n Bytes sent in message was : " + str(bytes))
    text_file.write("\nTotal Data sent was : " + str(totalBytes) + " Bytes." )
    text_file.write("\nAverage RTT was : " + str (averageRTT) + " seconds." )
    text_file.write("\nRequests was : " + str (totalRequests))
