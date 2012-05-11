#!/usr/bin/python2
from datetime import datetime
import smbc, logging

# smbc entry types
SMBC_FILE = 8L
SMBC_DIR = 7L
SMBC_SERVICE = 3L

def scan_host(host, mongo_collection):
    """ Scanning given host and save results in given mongo collection """

    mongo_collection.drop()

    smb_host = 'smb://' + host
    ctx = smbc.Context()


    item_type = lambda entry: 'file' if entry.smbc_type == SMBC_FILE else 'dir'

    def get_metainfo(path):
        data = ctx.stat(path)
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
        })


    def process_entry(root, dent):
        try:
            dent_type = item_type(dent)
            path = root + '/' + dent.name

            sum_size = None
            if dent_type == 'dir':
                sum_size = 0
                for entry in ctx.opendir(path).getdents():
                    if entry.name not in ['..', '.']:
                        sum_size += process_entry(path, entry)

            changed_at, size = get_metainfo(path)
            # Size of folder is sum of size of all files in it
            if sum_size <> None: size = sum_size
            save_object(path, dent_type, changed_at, size)

            return size

        except smbc.NoEntryError:
            logging.exception('No entry error: ' + path)
        except smbc.PermissionError:
            logging.exception('Permission error: ' + path)
        except:
            logging.exception('Unknown error: ' + path)

        return 0


    for entry in ctx.opendir(smb_host).getdents():
        if entry.smbc_type == SMBC_SERVICE:
            process_entry(smb_host, entry)
