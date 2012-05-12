from ..mongo_db import mdb, main_collection, servers_collection, split_words
from samba import scan_host
from datetime import datetime
from pymongo import binary
import hashlib, os, logging

def get_name(path):
    return os.path.split(path)[1]

def get_extension(path):
    split = get_name(path).split('.')
    if len(split) > 1: return split[-1].lower()
    

def get_unic_id(data):
    name = get_name(data['_id'])
    unic_str = name + u':' + str(data['sz']) + ':' + str(data['ch_t'])
    bin_string = hashlib.md5(unic_str.encode('utf8')).digest()
    return binary.Binary(bin_string, binary.MD5_SUBTYPE)

def update_host(host):
    server = servers_collection.find_one({'host': host})
    if server == None:
        server_id = str(servers_collection.save({'host': host}))
        server = servers_collection.find_one({'host': host})
    else:
        server_id = str(server['_id'])

    server['scan_start'] = datetime.now()

    col = mdb['host.' + str(server_id)]
    start_scan = datetime.now()

    print('Started scanning host: ' + host)
    resp = scan_host(host, col)
    # If failed to scan then mark as inactive
    if resp <> None:
        server['is_active'] = False
        servers_collection.save(server)
        print 'Marked host as inactive.'
        return
    else:
        server['is_active'] = True
        servers_collection.save(server)

    col.remove({'s_t': {'$l_t': start_scan}})

    print('Started postprocessing. Total entries at host: %d. Total entries in the main collection: %d' % (col.find().count(), main_collection.find().count()))
    ids = {}
    for entry in col.find():
        unic_id = get_unic_id(entry)

        if unic_id in ids:
            main_collection.update({'_id': unic_id}, {'$push': {'server.' + server_id: entry['_id']}, '$set': {'s_t': datetime.now()}}, multi=True)
        else:
            ids[unic_id] = entry
            # Overwiting path for this host
            resp = main_collection.update({'_id': unic_id}, {'$set': {'server.' + server_id: [entry['_id']]}, '$set': {'s_t': datetime.now()}}, safe=True, multi=True)
            # Creating new entry if was updated nothing
            if not resp['updatedExisting']:
                path = entry['_id']
                entry['srvs'] = {server_id: [path]}
                entry['wds'] = split_words(get_name(path).lower())
                entry['_id'] = unic_id
                entry['s_t'] = datetime.now()
                entry['nm'] = get_name(path)
                if entry['is_f']:
                    extension = get_extension(path)
                    if extension: entry['ext'] = extension
                main_collection.save(entry)

    server['scan_end'] = datetime.now()
    servers_collection.save(server)
    print('Finished. Total entries in the main collection: %d' % main_collection.find().count())