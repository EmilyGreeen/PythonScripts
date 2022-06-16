#!/usr/bin/python3

import os
import mysql.connector as database
from datetime import datetime

backupDir = '/home/backup/'


logdate = datetime.now()
logdate = str(logdate.year)+"-"+str(logdate.month)+"-"+str(logdate.day)+"-"+str(logdate.hour)+"h"


def archiveWebsite():
    os.system('cp -r /var/www/Basic-Website-using-HTML-CSS-master /home/backup')
    os.system('zip '+backupDir+'websiteArchive'+logdate+'.zip '+backupDir+'Basic-Website-using-HTML-CSS-master')
    os.system('rm -rf '+backupDir+'Basic-Website-using-HTML-CSS-master')

def archiveDatabase():
    try:
        connexion = database.connect(user ='root',
                                    password = '123',
                                    host = 'localhost',
                                    database = 'classicmodels')
        os.system('mysql -u root -p 123 classicmodels >'+backupDir+'classicmodels.sql' )
        os.system('zip '+backupDir+'databaseArchive'+logdate+'.zip '+backupDir+'classicmodels.sql')
        os.system('rm -rf '+backupDir+'classicmodels.sql')
        os.system('ls '+backupDir)

    except:
        print("connexion failed")

    