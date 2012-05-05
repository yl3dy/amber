#!/usr/bin/python2

"""

Start options:
    * no arguments - update all hosts
    * some arguments - all arguments are counted as hosts

Updating index - create new collection, then replace current with it
In database names . are replaced with ,

"""

from settings import *
import sys
from pymongo import Connection
from os.path import exists, join
from commands import getoutput

def addr2name(addr):
    return addr.replace('.', ',')

def init_host(host):
    services = []
    lines = getoutput('smbclient -g -N -L //'+host+'/')
    for line in lines.split('\n'):
        if line[0:4] == 'Disk':
            services.append(line.split('|')[1])
    return services

def mount_service(service, host):
    if not exists(MOUNT_PATH):
        os.mkdir(MOUNT_PATH)
    os.system('sudo -u '+USERNAME+' smbclient -o guest //'+host+'/ '+MOUNT_PATH)

def update_all_hosts():
    pass

def update_host(host):
    db = Connection()[addr2name(host)]
    storage = db['listing_new']
    storage_old = db['listing']

    #for service in init_host(host):
    #    mount_service(service, host)
    #    for root, dirs, files in os.walk(MOUNT_PATH):
    #        for f in files:
    #            storage.insert({
    #                            'path': join(root, f),
    #                            'type': 'file'
    #                           })
    #storage_old.drop()
    #storage.rename('listing')

if __name__ == '__main__':
    print('Oberon crawler v0.0.1')

    if len(sys.argv) < 2:
        print('Updating all hosts in DB')
        update_all_hosts()
    else:
        for host in sys.argv[1:]:
            print('Updating host ' + host)
            update_host(host)
