from django.shortcuts import render_to_response
from mongo_db import mdb, main_collection, servers_collection, split_words
from datetime import datetime
import os

RESULT_NUM = 100

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def get_paths(servers, paths):
    res = []
    for server_id in paths:
        server = servers[server_id]
        for path in paths[server_id]:
            res.append((
                server['is_active'],
                'smb://' + os.path.join(server['host'], path)
            ))
    return res

def get_servers():
    res = {}
    for server in servers_collection.find(): res[str(server['_id'])] = server
    return res

def postprocess_entry(servers, entry):
    return {
        'name': entry['nm'],
        'size': sizeof_fmt(entry['sz']),
        'paths': get_paths(servers, entry['srvs']),
        'is_file': entry['is_f'],
    }

def postprocess_results(results):
    servers = get_servers()
    res = [postprocess_entry(servers, entry) for entry in results]
    res.sort(key = lambda x: x['name'])
    return res
    

def mainpage(request):
    search_string = result = search_time = performance = None
    if request.method == 'GET' and 'q' in request.GET:
        search_string = request.GET.get('q', '')
        t = datetime.now()
        result = main_collection.find({'wds': {'$all': split_words(search_string.lower())}}).limit(RESULT_NUM)
        performance = result.explain()
        search_time = datetime.now() - t
    return render_to_response('main.html', {'search_result': postprocess_results(result), 'search_string': search_string, 'search_time': search_time, 'performance': performance})
