#!/usr/bin/python3

file = '/tmp/test.txt'
strToWrite = "One Line\nTwo Lines\n"

def init(file):
    with open(file, 'w') as f:
        f.write("Hello World\n\n")

def readFile(file):
    with open(file,'r') as t:
        print(t.read())
        

def writeFile(file,string):
    tmp = open(file,'a')
    tmp.write(string)
    tmp.close()

#init(file)
#for i in range(5):
#    writeFile(file,strToWrite)
#readFile(file)    

