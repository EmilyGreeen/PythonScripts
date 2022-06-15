#!/usr/bin/python3

from paramiko import SSHClient
import os

cwd = os.getcwd()+'/ssh/'

client = SSHClient()
client.load_system_host_keys()
client.load_host_keys('/home/emily/.ssh/known_hosts')

client.connect('localhost', username='emily', password='1234567')

stfp = client.open_sftp()
stfp.put('/home/emily/Python/day02/ssh/ssh.py','ssh.py')

stdin, stdout, stderr = client.exec_command("chmod u+x "+cwd+"info.py")
for line in stdout.read().splitlines():
    print(line)
for line in stderr.read().splitlines():
    print(line)
    
print()

stdin, stdout, stderr = client.exec_command("python3 "+cwd+"info.py")
for line in stdout.read().splitlines():
    print(line)
for line in stderr.read().splitlines():
    print(line)
    
client.close()