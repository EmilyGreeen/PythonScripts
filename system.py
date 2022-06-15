#!/usr/bin/python3

import platform
#import subprocess
import re,uuid
import socket
import os

my_system = platform.uname()

print(f"System: {my_system.system}")
print(f"Node Name: {my_system.node}")
print(f"Release: {my_system.release}")
print(f"Version: {my_system.version}")
print(f"Machine: {my_system.machine}")
print(f"Processor: {my_system.processor}")

#Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
#new = []

#for item in Id:
#    new.append(str(item.split("\r")[:-1]))
#for i in new:
#    print(i[2:-2])

print("My MAC address: ",end="")
print(':'.join(re.findall('..','%012x' % uuid.getnode())))

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your computer's name is : "+hostname)
print("Your computer IP address is : "+IPAddr)

cwd = os.getcwd()
print("Current working directory:",cwd)
os.chdir('/tmp')
cwd = os.getcwd()
print("Current working directory:",cwd)
print(os.listdir('/tmp'))
print()
#os.mkdir('/tmp/emily00000000000001')
print(os.listdir('/tmp'))
