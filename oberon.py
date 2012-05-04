#!/usr/bin/python2

"""

Start options:
    * no arguments - update all hosts
    * some arguments - all arguments are counted as hosts

Updating index - create new collection, then replace current with it

"""

import settings
import os
import sys
from pymongo import Connection

def mount_host(host):
    pass

def update_all_hosts():
    pass

def update_host(host):
    storage = Connection()[host]['listing_new']
    mount_host(host)

if __name__ == '__main__':
    print('Oberon crawler v0.0.1')
    
    if len(sys.argv) == 0:
        update_all_hosts()
    else:
        for host in sys.argv:
            update_host(host)
