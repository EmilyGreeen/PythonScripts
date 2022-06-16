#!/usr/bin/python3

from inspect import getfile
import os
import re
import datetime
from tabnanny import check
import paramiko

def sshSaveToArchive(host,port,username,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,port=port,username=username,password=password)

    os.system('sshpass -p '+password+' scp '+username+'@'+host+':/home/backup/*.zip /archivage')

    stdin, stdout, stderr = ssh.exec_command('rm -rf /home/backup/*.zip')
        

def getFileDate(file):
    filedate = re.search("[database][website]Archive(.*)h.zip",file)
    if not filedate:
        return -1
    return filedate.group(1)

def checkRententionTime(retention):
    
    today = datetime.datetime.now()
    files = os.listdir('/archivage/')
    
    for file in files:
        fileDate=getFileDate(file)
        print(fileDate)
        try:
            fileDateObj = datetime.datetime.strptime(fileDate, '%Y-%m-%d-%H')
        except:
            print()
        dateToKill = today - datetime.timedelta(weeks=retention)
        if fileDateObj < dateToKill:
            print("8 weeks or more have elapsed, archive too old, deleting")
            os.system('rm /archivage/'+file)
            

def main():
    ARCHIVE_RETENTION_TIME = 8 #eight weeks

    host = "SRV-web"
    port = 22
    username = "debian"
    password = "azerty"
        
    sshSaveToArchive(host,port,username,password)
    checkRententionTime(ARCHIVE_RETENTION_TIME)

main()