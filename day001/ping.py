#!/usr/bin/python3


import os

target = "8.8.8.8"
resp = os.system("ping -c 1 " + target)

if resp == 0:
  print('\n', target, 'is up!')
else:
  print('\n', target, 'is down!')