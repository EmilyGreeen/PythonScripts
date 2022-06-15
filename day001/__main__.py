   #!/usr/bin/python3

from sys import exit
from script import main

log = '/tmp/sys.log'
mailFlag = 0

if __name__ == '__main__':
    exit(main(log, mailFlag))