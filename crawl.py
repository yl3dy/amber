#!/usr/bin/python2

import sys
from amber.crawler import updater

if __name__ == '__main__':
    if len(sys.argv) == 2:
        updater.update_host(sys.argv[1])
    else:
        print 'Please enter host as the only command line argument'
