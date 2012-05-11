#!/usr/bin/python2
from datetime import datetime
import smbc

# smbc entry types
SMBC_FILE = 8L
SMBC_DIR = 7L
SMBC_SERVICE = 3L

def host_scanner(host, mongo_collection):
    """ Generator to walk around SMB tree """

    mongo_collection.drop()

    smb_host = 'smb://' + host
    ctx = smbc.Context()


    item_type = lambda entry: 'file' if entry.smbc_type == SMBC_FILE else 'dir'

    def get_metainfo(path):
        data = ctx.open(path).fstat()
        return 0, 1

    def save_object(path, dent_type, change_time, size=None):
        data = {
            '_id': path.replace(smb_host + '/', ''), # Path without host will be object id
            'is_f': True if dent_type == 'file' else False, # Is object has hile type
            'ch_t': change_time,   # Object change time
            's_t': datetime.now(), # Save time
        }
        if size: data['sz'] = size # Size of the object if given 
        mongo_collection.save(data)

    def process_entry(root, dent):
        try:
            dent_type = item_type(dent)
            path = root + '/' + dent.name

            changed_at = None
            if dent_type == 'dir':
                for entry in ctx.opendir(path).getdents():
                    if entry.name not in ['..', '.']:
                        entry_time = process_entry(path, entry)

                        if changed_at == None or changed_at < entry_time: changed_at == entry_time

                # If time is None then directory does not contain files, so we ommit it
                if changed_at <> None:
                    save_object(path, dent_type, changed_at)

            elif dent_type == 'file':
                changed_at, size = get_metainfo(path)
                save_object(path, dent_type, changed_at, size)
            return changed_at
        except smbc.NoEntryError:
            print('No entry error: ' + path)
        except smbc.PermissionError:
            print('Permission error: ' + path)
        except:
            print('Unknown error: ' + path)

    for entry in ctx.opendir(smb_host).getdents():
        if entry.smbc_type == SMBC_SERVICE:
            process_entry(smb_host, entry)
