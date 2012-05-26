from ..mongo_db import main_collection, split_words
from datetime import datetime
import logging


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
