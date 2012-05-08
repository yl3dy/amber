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
import smbc

# smbc entry types
SMBC_FILE = 8L
SMBC_DIR = 7L
SMBC_SERVICE = 3L

def addr2name(addr):
    return addr.replace('.', ',')

def update_all_hosts():
    pass

def update_host(host):
    def smb_walk(ctx, host):
        """ Generator to walk around SMB tree """
        cache = [ [], ]
        item_type = lambda entry: 'file' if entry.smbc_type == SMBC_FILE else 'dir'

        # initial filling of cache
        for item in ctx.opendir('smb://'+host+'/').getdents():
            if item.smbc_type == SMBC_SERVICE:
                cache[0].append(('smb://'+host+'/'+item.name, item_type(item)))
        while cache != []:
            item = cache[-1].pop()
            yield item
            if item[1] == 'dir':
                try:
                    tmp = []
                    for entry in ctx.opendir(item[0]).getdents():
                        if (entry.name <> '..') and (entry.name <> '.'):
                            tmp.append((item[0]+'/'+entry.name, item_type(entry)))
                    cache.append(tmp)
                except smbc.PermissionError:
                    pass
                except smbc.NoEntryError:
                    print('Can\'t read entry named '+item[0])
                except:
                    print('Random fail has happened on entry '+item[0]+' which is '+item[1])
            while cache and cache[-1] == []: 
                cache.pop()

    print('Updating host ' + host)
    db = Connection()[addr2name(host)]
    storage = db['listing_new']
    storage_old = db['listing']
    ctx = smbc.Context()

    for entry in smb_walk(ctx, host):
        entryname = os.path.split(entry[0])[1]
        storage.insert({
                        '_id': entry[0],
                        'name': entryname,
                        'subnames': entryname.lower().split(' '),
                        'type': entry[1],
                       })
    storage.rename('listing', dropTarget=True)

if __name__ == '__main__':
    print('Oberon crawler v0.0.1')

    if len(sys.argv) < 2:
        print('Updating all hosts in DB')
        update_all_hosts()
    else:
        for host in sys.argv[1:]:
            update_host(host)
