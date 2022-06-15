#!/usr/bin/python3

import multiprocessing
import time
import socket
import subprocess
import sys
from datetime import datetime
from typing import final

#Clear the screen
subprocess.call('clear', shell=True)

#Ask for input
if 'i' == input("by hostname[H] or IP[i]?"):
    remoteServerIP = input("Enter a remote IP to scan: ")
else:
    remoteServer    = input("Enter a remote host to scan: ")
    remoteServerIP  = socket.gethostbyname(remoteServer)

#Print a nice banner with info on which host we are about to scan
print('-' * 60)
print("Please wait, scanning remote host", remoteServerIP)
print('-' * 60)

#check what time the scan started
t1 = datetime.now()

#Using the range function to specify ports (here it will scan
# all ports between 1 and 1024)

#We also put in some error handling for catching errors

def scanPort(remoteServerIP, port, return_dict):
        result = sock.connect_ex((remoteServerIP, port))
        return_dict[result] = result
       

openPorts = [] 
PORTRANGE = [0,0]
PORTRANGE[0] = 1
PORTRANGE[1] = 20

try:
    for port in range(PORTRANGE[0],PORTRANGE[1]):
        #flag to check if timedout
        timedout=False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #process manager to get result of scanPort function
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        job=[]
        
        #init scanPort process to be able to close it if take more than 1s
        result = multiprocessing.Process(target=scanPort, args=(remoteServerIP, port, return_dict))
        job.append(result)
        result.start()
        
        joined=True
        if joined:
            result.join(1)
        
            #if process alive (not finished) kill process and print result
            if result.is_alive():
                print ("Port {}:    Closed (Timed out)".format(port))
                result.terminate()
                timedout=True
                sock.close()
                continue
        
        #Get result values from manager after process done 
        for proc in job:
            proc.join()
        
        finalRes=return_dict.values()[0]
            
        if finalRes == 0:
            print ("Port {}:    Open".format(port))
            openPorts.append(port)
        else:
            if not timedout:
                print ("Port {}:    Closed".format(port))
        sock.close()
        
except KeyboardInterrupt:
    print ("You pressed ctrl+C")

except socket.gaierror:
    print('Hostname could not be resolved. Exiting.')

except socket.error:
    print("Couldnt connect to server")
    sys.exit()
    

print("Range scanned on ",str(remoteServerIP),": ",str(PORTRANGE[0])," - ",str(PORTRANGE[1]))
print("Number of ports opened: ",openPorts.__len__())
if openPorts.__len__() != 0:
    print("Ports opened :")
    for port in openPorts:
        print("\t-",port)

#Checking the time again
t2 = datetime.now()

#Calculates the difference of time, to see how long it took to run
#the script
total = t2-t1

#Printing the information to screen
print('Scanning completed in: ',total)