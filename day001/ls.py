#!/usr/bin/python3

import os

def printDir(path):
    tmp = os.listdir(path)
    for i in tmp:
        print(i)

printDir("/dev")
print("-------------------")
 

printDir("/tmp")
print("-------------------")

try:   
    os.mkdir('/tmp/emily')
    printDir("/tmp")
except:
    print("Error while creating /tmp/emily")
print("-------------------")

try:
    os.mkdir('/tmp/emily/brico')
    printDir("/tmp/emily")
except:
    print("Error while creating /tmp/emilybrico")
print("-------------------")

try:
    os.mkdir('/tmp/emily/brico/a')
    os.mkdir('/tmp/emily/brico/b')
    printDir("/tmp/emily/brico")
except:
    print("Error while creating /tmp/emilybrico/{a,b}")
print("-------------------")

import shutil
try:
    shutil.rmtree('/tmp/emily/brico')
    printDir("/tmp/emily")
except:
    print("Error while deleting folder and its children")
print("-------------------")

try:
    if not os.path.isdir('/tmp/a/'):
        os.makedirs('/tmp/a/b/c/d')
    printDir("/tmp")
    printDir("/tmp/a")
    printDir("/tmp/a/b")
    printDir("/tmp/a/b/c")
except:
    print('Error while creating /tmp/a/b/c/d')
print("-------------------")

try:
    if os.path.isdir('/tmp/z'):
        shutil.rmtree('/tmp/z')
    os.rename('/tmp/a','/tmp/z')
    printDir("/tmp")

except:
    print("something went wrong")
print("-------------------")