#!/usr/bin/python2
from datetime import datetime
import smbc, logging

MAX_TRIES = 5

# smbc entry types
SMBC_FILE = 8L
SMBC_DIR = 7L
SMBC_SERVICE = 3L

ENCODE_TABLE = {
    '!': '%21',
    '&': '%26',
    '?': '%3F',
    '%': '%25',
    '~': '%7E',
    '[': '%5B',
    ']': '%5D',
}

def item_type(entry):
    return 'file' if entry.smbc_type == SMBC_FILE else 'dir'

def is_service(entry):
    return entry.smbc_type == SMBC_SERVICE


def percent_encode(string):
    result = ''
    for i in range(len(string)):
        if string[i] in ENCODE_TABLE:
            result += ENCODE_TABLE[string[i]]
        else:
            result += string[i]
    return result



def get_dents(ctx, path):
    return ctx.opendir(percent_encode(path)).getdents()

def get_metainfo(ctx, path):
    data = ctx.stat(percent_encode(path))
    change_time = datetime.fromtimestamp(data[8])
    size = data[6]
    return change_time, size


def process_entry(input_pipe, ctx, root, dent, trying=0):
    path = None
    size = 0
    try:
        path = root + '/' + dent.name
        dent_type = item_type(dent)

        sum_size = None
        if dent_type == 'dir':
            sum_size = sum([
                process_entry(input_pipe, ctx, path, entry)
                for entry in get_dents(ctx, path)
                if entry.name not in ['..', '.']
            ])

        changed_at, size = get_metainfo(ctx, path)

        # Size of folder is sum of size of all files in it
        if sum_size <> None: size = sum_size
        if dent_type == 'dir': path += '/'

        data = {
            'path': path.decode('utf8'),
            'size': size,
            'changed_at': changed_at,
            'is_file': dent_type == 'file',
        }

        if input_pipe: input_pipe.send(data)
        else: print data

        return size

    except smbc.NoEntryError:
        logging.error('No entry error: ' + str(path))
    except smbc.PermissionError:
        logging.error('Permission error: ' + str(path))
    except smbc.TimedOutError:
        logging.error('Timed out error: ' + str(path))
    except Exception as err:
        logging.exception('Unknown exception: ' + str(path))

    if trying < MAX_TRIES: size = process_entry(input_pipe, ctx, root, dent, trying+1)

    return size

def scan_host(host, input_pipe=None):
    """ Scanning given host and snd data to return pipe if given """

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
        return False

    for entry in entries: process_entry(input_pipe, ctx, smb_host, entry)

    if input_pipe: input_pipe.send(None)
    else: print 'Finished.'

    return True
