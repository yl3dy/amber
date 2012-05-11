#!/usr/bin/python2
from django.conf import settings

mdb = pymongo.Connection(settings.MONGODB['connection'])[settings.MONGODB['database_name']]
