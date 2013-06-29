'''Functions and variables for working with Mongo DB'''
from amber import settings
import pymongo

MDB = pymongo.Connection(
    settings.MONGO_DB['connection'])[settings.MONGO_DB['database_name']]

MAIN_COLLECTION = MDB['main']

SERVERS_COLLECTION = MDB['servers']

def split_words(name):
    '''Splitting words in the given name'''
    name = name.lower()
    result = []
    start = 0
    for i in xrange(len(name)):
        if name[i] in settings.WORD_DELIMITERS:
            if start != i:
                result.append(name[start:i])
            start = i + 1
    if name[start:]:
        result.append(name[start:])
    return result
