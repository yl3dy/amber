#!/usr/bin/python2
from datetime import datetime
import smbc, logging
from tools import get_unic_id, is_service, item_type, percent_encode

MAX_TRIES = 5

def get_dents(ctx, path):
    return ctx.opendir(percent_encode(path)).getdents()

def get_metainfo(ctx, path):
    data = ctx.stat(percent_encode(path))
    change_time = datetime.fromtimestamp(data[8])
    size = data[6]
    return change_time, size

def save_object(path, dent_type, change_time, size):
    mongo_collection.save({
        '_id': path.replace(smb_host + '/', ''), # Path without host will be object id
        'is_f': True if dent_type == 'file' else False, # Is object has hile type
        'sz': size,
        'ch_t': change_time,   # Object change time
        's_t': datetime.now(), # Save time
        'uid': get_unic_id(path, size, change_time), # Unic identificator
    })



def process_entry(ctx, root, dent, trying=0):
    path = None
    size = 0
    try:
        path = root + '/' + dent.name
        dent_type = item_type(dent)

        sum_size = None
        if dent_type == 'dir':
            sum_size = sum([
                process_entry(ctx, path, entry)
                for entry in get_dents(ctx, path)
                if entry.name not in ['..', '.']
            ])

        changed_at, size = get_metainfo(ctx, path)
        # Size of folder is sum of size of all files in it
        if sum_size <> None: size = sum_size
        save_object(path, dent_type, changed_at, size)

        return size

    except smbc.NoEntryError:
        logging.error('No entry error: ' + path)
    except smbc.PermissionError:
        logging.error('Permission error: ' + path)
    except smbc.TimedOutError:
        logging.error('Timed out error: ' + path)
    except Exception as err:
        logging.exception('Unknown exception: ' + path)

    if trying < MAX_TRIES: size = process_entry(ctx, root, dent, trying+1)

    return size

def scan_host(host, mongo_collection):
    """ Scanning given host and save results in given mongo collection """

    mongo_collection.drop()

    smb_host = 'smb://' + host
    ctx = smbc.Context()


    entries = []
    try:
        entries = [
            entry
            for entry in ctx.opendir(smb_host).getdents()
            if is_service(entry)
        ]
    except Exception as err:
        logging.exception('Failed to scan host: ' + smb_host)
        return 'fail'

    for entry in entries: process_entry(ctx, smb_host, entry)
