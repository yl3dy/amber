# -*- coding: utf-8 -*-
'''Functions for working with servers'''
from ..mongo_db import SERVERS_COLLECTION
import base64, struct, logging

def encode64(num):
    '''Encoding given number into base64'''
    data = struct.pack('<Q', num).rstrip('\x00')
    if len(data)==0:
        data = '\x00'
    return base64.urlsafe_b64encode(data).rstrip('=')
 
def decode64(string):
    '''Decoding given string into number'''
    data = base64.urlsafe_b64decode(str(string) + '==')
    return struct.unpack('<Q', data + '\x00'* (8-len(data)))[0]

def get_new_id():
    '''Return new server id'''
    int_ids = [decode64(server['_id']) for server in SERVERS_COLLECTION.find()]
    if not int_ids:
        return encode64(0)
    int_ids.sort()
    return encode64(int_ids[-1] + 1)



def get_server_id(host, auto_names=False, name=None):
    '''Return server id by given host name'''
    logging.info('Getting server id')
    server = SERVERS_COLLECTION.find_one({'host': host})

    # prepare server name
    if auto_names:
        server_name = host.split('.')[0]
    else:
        if name:
            server_name = name
        else:
            server_name = host

    if server == None:
        server_id = get_new_id()
        logging.info('Creating new server (host: %s, id %s)', host, server_id)
        SERVERS_COLLECTION.save({
            '_id': server_id,
            'name': host,
            'host': host,
            'is_active': False,
            'scan_start': None,
            'scan_end': None,
        })
    else:
        server_id = server['_id']

    update_server_info(server_id, {'name': server_name})
    return server_id

def update_server_info(server_id, data):
    '''Updating server info by given data'''
    logging.info('Updating server info')
    SERVERS_COLLECTION.update({'_id': server_id}, {'$set': data})
