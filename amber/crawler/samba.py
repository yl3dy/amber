# -*- coding: utf-8 -*-
'''Scanning samba shares'''
from datetime import datetime
import smbc, logging
from multiprocessing import Queue, Process
from time import sleep
import os.path

PROCESS_NUMBER = 3
SLEEP_TIME = 5

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


def percent_encode(string):
    '''Percent encoding of given string'''
    result = ''
    for i in range(len(string)):
        if string[i] in ENCODE_TABLE:
            result += ENCODE_TABLE[string[i]]
        else:
            result += string[i]
    return result

def data_process(q_in, q_out):
    '''Scanning process, which using pipes for getting and returning data'''
    ctx = smbc.Context()
    while True:
        entry = q_in.get()

        if entry == None:
            break

        path = entry[0]
        is_file = entry[1]

        change_time = size = childs = None

        try:
            data = ctx.stat(percent_encode(path))
            change_time = datetime.fromtimestamp(data[8])
            size = data[6]

            childs = None
            if not is_file:
                childs = [
                    (path + '/' + dent.name, dent.smbc_type == SMBC_FILE)
                    for dent in ctx.opendir(percent_encode(path)).getdents()
                    if dent.name not in ['..', '.']
                ]
            q_out.put((path, is_file, change_time, size, childs))
        except smbc.TimedOutError:
            print 'Some sleep... at: ' + path
            sleep(SLEEP_TIME)
            q_in.put(entry)
        except smbc.PermissionError:
            logging.info('Permission error at: ' + path)
            q_out.put(None)
        except smbc.NoEntryError:
            logging.info('No entry error at: ' + path)
            q_out.put(None)
        except Exception:
            logging.exception('\n\n====================\nException at: ' + path)
            q_out.put(None)
        

def get_data(q_in, q_out, entries):
    '''Getting data'''
    res = []
    for entry in entries:
        q_in.put(entry)
    for entry in entries:
        res.append(q_out.get())
    return res


def process_childs(input_pipe, q_in, q_out, entries, host):
    '''Processing childs'''
    sum_size = 0
    for entry in get_data(q_in, q_out, entries):
        if entry == None:
            continue
        path, is_file, change_time, size, childs = entry

        if not is_file:
            size = process_childs(input_pipe, q_in, q_out, childs, host)

        sum_size += size

        data = {
            'path': path.decode('utf8').replace(host, ''),
            'size': size,
            'change_time': change_time,
            'is_file': is_file,
        }

        if input_pipe:
            input_pipe.send(data)
        else:
            print data['path']

    return sum_size


def scan_host(host, index_path, input_pipe=None):
    '''Scanning given host and snd data to return pipe if given'''

    smb_host = 'smb://' + host
    ctx = smbc.Context()


    entries = []
    try:
        if not index_path:
            entries = [
                (smb_host + '/' + entry.name, False)
                for entry in ctx.opendir(smb_host).getdents()
                if entry.smbc_type == SMBC_SERVICE
            ]
        else:
            entries = [ (os.path.join(smb_host, index_path), False), ]
    # TODO Specify exceptions
    except Exception:
        if input_pipe:
            input_pipe.send(None)
        else:
            print 'Finished.'
        logging.exception('Failed to scan host: ' + smb_host)
        return False
 
    # Queues for interacting with processes
    q_in = Queue()
    q_out = Queue()
    # Creating list of samba processors with own samba context
    processes = [
        Process(target=data_process, args=(q_in, q_out))
        for _ in xrange(PROCESS_NUMBER)
    ]
    for process in processes:
        process.start()

    process_childs(input_pipe, q_in, q_out, entries, smb_host)

    # Sending messages to stop processes
    for process in processes:
        q_in.put(None)
    for process in processes:
        process.join()

    if input_pipe:
        input_pipe.send(None)
    else:
        print 'Finished.'

    logging.info('Finished scanning server')

    return True
