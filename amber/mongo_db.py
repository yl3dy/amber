#!/usr/bin/python2
from django.conf import settings
import pymongo

mdb = pymongo.Connection(settings.MONGO_DB['connection'])[settings.MONGO_DB['database_name']]

main_collection = mdb['main_collection']

servers_collection = mdb['servers']

# Temporarly will be placed here
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
