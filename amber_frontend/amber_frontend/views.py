from django.http import HttpResponse
from django.shortcuts import render_to_response
import pymongo
import re
from datetime import datetime

SERVER_NAMES = ('stonehenge-3,sytes,net','dgap-gw,campus')
RESULT_NUM = 100

def search(query):
    system = pymongo.Connection()
    results = []
    for dbname in SERVER_NAMES:
        s_r = system[dbname]['listing'].find({'subnames': query.lower()}).limit(RESULT_NUM - len(results))
        results += list(s_r)
    return results, s_r.explain()

def mainpage(request):
    search_string = search_output = search_time = performance = None
    if request.method == 'GET' and 'q' in request.GET:
        search_string = request.GET.get('q', '')
        t = datetime.now()
        search_output,performance = search(search_string)
        search_time = datetime.now() - t
    return render_to_response('index.html', {'search_output': search_output, 'search_string': search_string, 'search_time': search_time, 'performance': performance})
