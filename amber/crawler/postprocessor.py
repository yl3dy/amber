from ..mongo_db import main_collection
from samba import scan_host
from datetime import datetime
from pymongo import binary
import hashlib, os, logging

    
DELIMITERS = (' ', '.', '-', '_', ',', '[', ']', '(', ')', '?', '!', '<', '>', '{', '}', '"', "'")

def split_words(name):
    result = []
    start = 0
    for i in xrange(len(name)):
        if name[i] in DELIMITERS:
            if start != i:
                result.append(name[start:i])
            start = i + 1
    if name[start:]: result.append(name[start:])
    return result

def get_extension(name):
    split = name.split('.')
    if len(split) > 1: return split[-1].lower()


def postprocessing(server_id, collection, scan_start):

    logging.info('Started postprocessing. Total entries: %d' % collection.find().count())
    logging.info('In the main collection: %d' % main_collection.find().count())
    for entry in collection.find():
        data = {
            '_id': entry['_id'],
            'n': entry['name'],
            'w': split_words(entry['name']),
            's': entry['size'],
            'f': entry['is_file'],
            'c': entry['change_time'],
        }
        if entry['is_file']: data['e'] = get_extension(entry['name'])

        paths = entry['paths']
        paths.sort()

        update_data = {'$set': {'p.' + server_id: paths, 't.' + server_id: datetime.now()}}

        main_collection.update(data, update_data, upsert=True)

    logging.info('Finished processing entries. Total objects in the main collection: %d' % main_collection.find().count())

    main_collection.update({'t.' + server_id: {'$lt': scan_start}}, {'$unset': {'p.' + server_id: 1, 't.' + server_id: 1}}, multi=True)
    main_collection.remove({'p': {}})

    logging.info('Finished postprocessing. Total objects in the main collection: %d' % main_collection.find().count())
