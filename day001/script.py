#!/usr/bin/python3

#affichage de 
#   -hostname
#   -cpu
#   -memory
#   -hard disk
#   -OS
#   -IP
#   -services
#
#then stock into file

import os
import sys
from file import writeFile, readFile
import platform
import socket
import psutil
import subprocess
import mysql.connector as database
import datetime
import smtplib
import requests
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Defines log to write to
#log = '/tmp/sys.log'
#mailFlag = 0
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def sendMail(file):
    """
    function to send mail and attache log file

    Args:
        file (file): log file to attach to mail
    """
    sender_email = "emgreendev@outlook.fr"
    receiver_email = sender_email
    
    msg = MIMEMultipart()
    msg['Subject'] = 'ALERT'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    msgText = MIMEText('<b>ALERTS HAVE BEEN RAISED IN LOG FILE</b>', 'html')
    msg.attach(msgText)
    msg.attach(MIMEText(open(file).read()))
    
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(sender_email, "p3JpBW7jVpK8q62")
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info("mail sent")
    except Exception as e:
        logging.error(e)


def clear():
    """function to easily clear the screen
    """
    subprocess.call('clear', shell=True)


def socketUse(log):
    """Gets basic info on hostname and ip address

    Args:
        log (file): log file in which to store data
    """
    hostname = socket.gethostname()
    writeFile(log,"Hostname: "+hostname+"\n")
    writeFile(log,"IP Address: "+socket.gethostbyname(hostname)+"\n")


def platformUse(log):
    """Gets info on OS
    
    Args:
        log (file): log file in which to store data
    """
    my_system = platform.uname()
    syst = f"System: {my_system.system}"
    node = f"Node Name: {my_system.node}"
    release = f"{my_system.release}"
    processor = f"Processor: {my_system.machine}"
    writeFile(log, syst+"\n")
    writeFile(log, node +" "+ release+"\n")
    writeFile(log, processor+"\n")


def psutilUse(log, mailFlag):
    """Gets Virtual Memory usage, Disk usage and CPU usage
    
    Args:
        log (file): log file in which to store data
        mailFlag (int): flag used as bool to signal sending mail

    Returns:
        int: signal send mail
    """
    
    #Section title
    writeFile(log, "-"*5+"MEM, DISK, CPU"+"-"*5+"\n")
    
    #Set threshold value to X%
    PERCENTTHRESHOLD = 0.65
    writeFile(log, 'using '+str(PERCENTTHRESHOLD*100)+"""% as threshold\n\n""")
    
    #Chapter Title
    writeFile(log, "-"*3+"MEMORY"+"-"*3+"\n")
    #Check and save virtual memory values
    TM = psutil.virtual_memory().total/(1024*1024*1024)
    totalTM = "Total Memory on / Partition: "+str(TM)+" GB"
    AM = psutil.virtual_memory().available/(1024*1024*1024)
    totalAM = "Memory Currently Available / Partition: "+str(AM)+" GB"
    writeFile(log, totalTM+"\n")
    writeFile(log, totalAM+"\n")
    #Check if available memory > total memory, if so, flag to send mail raised
    if AM > TM*PERCENTTHRESHOLD:
        writeFile(log, "###!!!###\nHIGH MEMORY USE\n\n")
        mailFlag = 1
    
    writeFile(log, "\n"+"-"*3+"DISK"+"-"*3+"\n")
    #Check and save disk capacity values
    TD = psutil.disk_usage('/').total/(1024*1024*1024)
    totalTD = "Disk Capacity: "+str(TD)+" GB"
    AD = psutil.disk_usage('/').free/(1024*1024*1024)
    totalAD = "Available Disk Capacity: "+str(AD)+" GB"
    rmF = "df -h :\n"+subprocess.run(['df', '-h'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    writeFile(log, totalTD+"\n")
    writeFile(log, totalAD+"\n")
    writeFile(log, rmF+"\n")
    #Check if available  disk capacity > total capacity, if so, flag to send mail raised
    if AD > TD*PERCENTTHRESHOLD:
        writeFile(log, "###!!!###\nLOW AVAILABLE SPACE ON DISK\n\n")
        mailFlag = 1
    
    #Chapter Title
    writeFile(log, "-"*3+"CPU"+"-"*3+"\n")
    #Check and save cpu use values
    numCPU = "Number of logical CPUs :"+str(psutil.cpu_count(logical=True))
    use = psutil.cpu_percent(interval=1)
    useCPU = "Current % of CPU use: "+str(use)
    writeFile(log, numCPU+"\n")
    writeFile(log, useCPU+"\n")
    #Check if CPU use > threshold, if so, flag to send mail raised
    if use > 100 * PERCENTTHRESHOLD:
        writeFile(log, "###!!!###\nHIGH CPU USE\n\n")
        mailFlag = 1
    
    return mailFlag


def getServiceState(log,serviceStr,mailFlag):
    """general function to test and save result of service status

    Args:
        log (file): log file in which to store data
        serviceStr (str): service name
        mailFlag (int): flag used as bool to signal sending mail

    Returns:
        int: signal send mail
    """
    
    #db services have different status outputs
    head = 5 if serviceStr == "mariadb" or serviceStr == "mysql" else 3
    
    service =  os.popen('echo | systemctl status '+serviceStr+'.service | head -n '+str(head)+' | tail -n 1')
    outputService = serviceStr+" service state :"+service.read()
    logging.info("check status "+serviceStr+" done")
    #if service inactive (dead), raise mail flag
    if "dead" in outputService:
        mailFlag = 1
        writeFile(log, "###!!!###\n"+serviceStr+" SERVICE INACTIVE\n\n")
    writeFile(log, outputService+"\n")
    writeFile(log,"\n")
    return mailFlag


def servicesState(log, mailFlag):
    """Gets info on network and services running currently

    Args:
        log (file): log file in which to store data
        mailFlag (int): flag used as bool to signal sending mail

    Returns:
        int: signal send mail
    """
    #get basic info for network tests
    hostname = socket.gethostname()
    ip = socket.gethostbyname(socket.gethostname())
    logging.info("ip get done")
    
    
    #Websites to test connection to
    WEBTEST = [ip,"google.fr","amazon.fr","ebay.com","discord.com","208.67.222.222","badwebsite.test"]

    #Section title
    writeFile(log, "\n"+"-"*5+"PING, HTTP, SSL"+"-"*5+"\n\n")
    
    #Chapter Title
    writeFile(log, "-"*3+"PING"+"-"*3+"\n\n")
    #test and save result of ping to websites
    webFlag = 0
    for web in WEBTEST:
        pingWeb = subprocess.run(['ping','-c','4', web], stdout=subprocess.PIPE).stdout.decode('utf-8')
        #if ping to web failed, add one to web flag
        if not pingWeb or "100% packet loss" in pingWeb:
            webFlag += 1
            outputPingWeb = "###!!!###\nPING TO "+web+" FAILED\n"
            logging.info("ping to "+web+" failed")
        else: 
            pingWeb = pingWeb.splitlines()[6:]
            outputPingWeb = "\n".join(pingWeb)+"\n"
            logging.info("ping to "+web+" done")
        writeFile(log, outputPingWeb)
        writeFile(log,"\n")
        
    #if all pings failed raise mail flag
    if webFlag == WEBTEST.__len__():
        writeFile(log,"###!!!###\nALL PINGS TO TEST WEBSITES FAILED\n\n")
        mailFlag = 1
    writeFile(log,"\n")
    logging.info("ping internet done")
    
    
    #Chapter Title
    writeFile(log, "-"*3+"HTTP"+"-"*3+"\n")
    #test and save result of http get requests to websites
    httpFlag = 0
    for web in WEBTEST:
        try:
            r = requests.get("http://"+web)
        except Exception as e:
            logging.info(e)
            r = -1
        if "200" in str(r):
            outputHttpWeb = "http get to "+web+": "+str(r)+" OK\n"
            logging.info("http get to http://"+web+" done -- "+outputHttpWeb)
        else:
            httpFlag += 1
            outputHttpWeb = "###!!!###\nHTTP GET TO http://"+web+" FAILED\nhttp get : "+str(r)+"\n"
            logging.info("http get to http://"+web+" failed -- "+outputHttpWeb)
        writeFile(log, outputHttpWeb)
        writeFile(log,"\n")
        
    #if all pings failed raise mail flag
    if httpFlag == WEBTEST.__len__():
        writeFile(log,"###!!!###\nALL HTTP GET TO TEST WEBSITES FAILED\n\n")
        mailFlag = 1
    writeFile(log,"\n\n")
    logging.info("http get internet done")            
    
    
    #Chapter Title
    writeFile(log, "-"*3+"SSL"+"-"*3+"\n")
    #test and save result of ssl connexion to google.fr
    sslFlag = 0
    for web in WEBTEST:
        sslCmd = os.popen('echo | openssl s_client -verify_quiet -showcerts -connect '+web+':443 | grep \"CONNECTED\"')
        ssl= sslCmd.read()
        #if ssl connection failed, add one to ssl flag
        if not ssl:
            sslFlag += 1
            writeFile(log, "###!!!###\nSSL TEST FAILED\n")
            outputSSL ="SSL test to "+web+" failed\n"
        else:
            outputSSL ="SSL test to "+web+": "+ssl
        writeFile(log, outputSSL)
        writeFile(log,"\n")
    
    #if all connection failed raise mail flag
    if sslFlag == WEBTEST.__len__():
        writeFile(log,"###!!!###\nALL SSL TESTS TO TEST WEBSITES FAILED\n\n")
        mailFlag = 1
    writeFile(log,"\n\n")
    logging.info("check ssl done")
    
    
    #Section Title
    writeFile(log, "-"*5+"SERVICES"+"-"*5+"\n")
    #Call to function checking for status of statuses in serviceArray
    serviceArray = ["mariadb","ssh","apache2","mysql"]
    flagArray = []
    for i in serviceArray:
        flagArray.append(getServiceState(log,i,mailFlag))
    
    if 1 in flagArray:
        mailFlag = 1
    
    
    return mailFlag


def tryDBConnection(log,mailFlag):
    """test our connection to specified database

    Args:
        log (file): log file in which to store data
        mailFlag (int): flag used as bool to signal sending mail

    Returns:
        int: signal send mail
    """
    #Section Title
    writeFile(log, "-"*5+"DATABASE CONNECTION"+"-"*5+"\n")
    DB = "sakila"
    try:
        connection = database.connect(	user="root",
                                    password="root",
                                    host="localhost", 
                                    database=DB
                                    )
        writeFile(log, "connection to database "+DB+" successful\n")
    except Exception as e:
        writeFile(log, str(e))
        mailFlag = 1
    logging.info("database connection done")
    return mailFlag


def loadInto(log, mailFlag):
    """Calls all previous functions and loads them into log file

    Args:
        log (file): log file in which to store data
        mailFlag (int): flag used as bool to signal sending mail

    Returns:
        int: signal send mail
    """
    clear()
    with open(log,'w') as f:
        f.write("This is your Sys log:\n")
    writeFile(log, "Log Date: "+str(datetime.datetime.now())+"\n")
    writeFile(log,"\n")
    logging.info("title done")
    
    socketUse(log)
    writeFile(log,"\n")
    logging.info("socket done")
    
    platformUse(log)
    writeFile(log,"\n")
    logging.info("platform done")
    
    mailFlag1 = psutilUse(log,mailFlag)
    writeFile(log,"\n")
    logging.info("psutil done")
    
    mailFlag2 = servicesState(log,mailFlag)
    logging.info("service done")
    
    mailFlag3 = tryDBConnection(log,mailFlag)
    logging.info("service done")
    
    clear()
    readFile(log)
    
    #this lines ensures a previous flag isnt overwritten
    return max(mailFlag1,mailFlag2,mailFlag3)

def main(log, mailFlag):
    mailFlag = loadInto(log, mailFlag)

    if mailFlag:
        sendMail(log)
    
    return 0

