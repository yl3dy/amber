'''Postprocessing of scanned results'''
from ..mongo_db import MAIN_COLLECTION, split_words
from datetime import datetime
import logging


def get_extension(name):
    '''Returns extension by given file name'''
    split = name.split('.')
    if len(split) > 1:
        return split[-1].lower()


def postprocessing(server_id, collection, scan_start):
    '''Postprocessing results in given collection for given server'''
    count = collection.find().count()
    logging.info('Started postprocessing. Total entries: %d', count)
    logging.info('In the main collection: %d', MAIN_COLLECTION.find().count())
    for entry in collection.find():
        data = {
            '_id': entry['_id'],
            'n': entry['name'],
            'w': split_words(entry['name']),
            's': entry['size'],
            'f': entry['is_file'],
            'c': entry['change_time'],
        }
        if entry['is_file']:
            data['e'] = get_extension(entry['name'])

        paths = entry['paths']
        paths.sort()

        update_data = {'$set': {
            'p.' + server_id: paths,
            't.' + server_id: datetime.now()
        }}

        MAIN_COLLECTION.update(data, update_data, upsert=True)

    count = MAIN_COLLECTION.find().count()
    logging.info('Finished processing. Total in the main: %d', count)

    MAIN_COLLECTION.update(
        {'t.' + server_id: {'$lt': scan_start}},
        {'$unset': {'p.' + server_id: 1, 't.' + server_id: 1}},
        multi=True
    )
    MAIN_COLLECTION.remove({'p': {}})

    count = MAIN_COLLECTION.find().count()
    logging.info('Finished postprocessing. Total in the main: %d', count)
