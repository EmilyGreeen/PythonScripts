#!/usr/bin/python3

from paramiko import SSHClient

client = SSHClient()
client.load_system_host_keys()
client.load_host_keys('/home/emily/.ssh/known_hosts')

client.connect('localhost', username='emily', password='1234567')
stdin, stdout, stderr = client.exec_command("ls /")
for line in stdout.read().splitlines():
    print(line)
for line in stderr.read().splitlines():
    print(line)
    
print()

stdin, stdout, stderr = client.exec_command("python3 --version")
for line in stdout.read().splitlines():
    print(line)
for line in stderr.read().splitlines():
    print(line)
    
client.close()
