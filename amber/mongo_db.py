#!/usr/bin/python2
from django.conf import settings
import pymongo

mdb = pymongo.Connection(settings.MONGO_DB['connection'])[settings.MONGO_DB['database_name']]

main_collection = mdb['main']

servers_collection = mdb['servers']
