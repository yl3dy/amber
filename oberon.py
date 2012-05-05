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
import os
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
    if os.system('smbmount -o guest //'+host+'/'+service+'/ '+MOUNT_PATH) == 0:
        return True
    else:
        return False

def umount_service():
    os.system('umount '+MOUNT_PATH)

def update_all_hosts():
    pass

def update_host(host):
    def add_entry(root, f=None):
        path = root.replace(MOUNT_PATH, '', 1)
        storage.insert({
                        '_id': os.path.join(path, f) if f else path,
                        'name': f if f else os.path.basename(path),
                        'type': 'file' if f else 'dir',
                       })

    print('Updating host ' + host)
    db = Connection()[addr2name(host)]
    storage = db['listing_new']
    storage_old = db['listing']

    for service in init_host(host):
        if not mount_service(service, host): continue
        for root, dirs, files in os.walk(MOUNT_PATH):
            for entry in files: add_entry(root, entry)
            add_entry(root)     # add current dir
        umount_service()

    #storage_old.drop()
    storage.rename('listing', dropTarget=True)

if __name__ == '__main__':
    print('Oberon crawler v0.0.1')

    if len(sys.argv) < 2:
        print('Updating all hosts in DB')
        update_all_hosts()
    else:
        for host in sys.argv[1:]:
            update_host(host)
