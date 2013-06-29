# -*- coding: utf-8 -*-
'''Views of site pages'''
from django.shortcuts import render_to_response
from amber.mongo_db import MAIN_COLLECTION, SERVERS_COLLECTION, split_words
from django.conf import settings
from datetime import datetime

def sizeof_fmt(num):
    '''Formatting file or folder size''' 
    for size in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, size)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

def get_paths(servers, paths, is_orthodox):
    '''Returm path links to given paths'''
    res = []
    if is_orthodox:
        url_prefix = 'smb://'
    else:
        url_prefix = 'file:////'
    for server_id in paths:
        server = servers[server_id]
        for path in paths[server_id]:
            res.append({
                'is_active': server['is_active'],
                'url': server['host'] + path,
                'urlprefix': url_prefix,
                'title': server['name' if 'name' in server else 'host'] + path,
            })
    return res

def get_servers(active_only=False):
    '''Returns servers list by ids'''
    res = {}
    if active_only:
        search_res = SERVERS_COLLECTION.find({'is_active': True})
    else:
        search_res = SERVERS_COLLECTION.find()
    for server in search_res:
        res[str(server['_id'])] = server
    return res

def postprocess_entry(servers, entry, is_orthodox):
    '''Postprocessing given entry, making usable names and formatted values'''
    return {
        'name': entry['n'],
        'size': sizeof_fmt(entry['s']),
        'paths': get_paths(servers, entry['p'], is_orthodox),
        'is_file': entry['f'],
    }



def get_entry_type_query(entry_type):
    '''Return query for given entry type'''
    if entry_type not in settings.ENTRY_TYPES:
        return {}
    entry_filter = settings.ENTRY_TYPES[entry_type]
    if 'is_file' in entry_filter:
        return {'f': entry_filter['is_file']}
    elif 'extensions' in entry_filter:
        return {'e': {'$in': entry_filter['extensions']}}
    return {}

def mainpage(request):
    '''Main page. Interface for performing search queries and viewing results'''
    servers = get_servers(active_only=True)
    response_dict = {
        'servers': servers,
        'entry_types': settings.ENTRY_TYPES,
    }

    if request.method == 'GET' and 'q' in request.GET and request.GET['q']:
        if 'windows' in request.META['HTTP_USER_AGENT'].lower():
            is_orthodox = False
        else:
            is_orthodox = True
        search_string = request.GET['q']
        server_request = request.GET.get('server', '')
        entry_type = request.GET.get('entry_type', '')

        response_dict.update({
            'search_string': search_string,
            'server_request': server_request,
            'entry_type': entry_type,
        })

        start_time = datetime.now()

        # Basic search through name, type and server
        search_dict = {'w': {'$all': split_words(search_string)}}
        if server_request:
            search_dict['p.' + server_request] = {'$exists': True}
        if entry_type:
            search_dict.update(get_entry_type_query(entry_type))
        result = MAIN_COLLECTION.find(search_dict)

        result = result.limit(settings.RESULT_NUM)
        # Choosing how to sort
        sort = {
            'name': None,
            'size': None,
            'change': None,
        }
        if 'sort_name' in request.GET:
            val = int(request.GET['sort_name'])
            result = result.sort('n', val)
            sort['name'] = val
        elif 'sort_size' in request.GET:
            val = int(request.GET['sort_size'])
            result = result.sort('s', val)
            sort['size'] = val
        elif 'sort_change' in request.GET:
            val = int(request.GET['sort_change'])
            result = result.sort('c', val)
            sort['change'] = val
        else:
            val = 1
            result = result.sort('n', val)
            sort['name'] = val

        response_dict['sort'] = sort

        # Setting output limit
        #result = result.limit(RESULT_NUM)

        # Looking into performance help if debugging
        #if settings.DEBUG: response_dict['performance'] = result.explain() 

        response_dict['search_result'] = [
            postprocess_entry(servers, entry, is_orthodox)
            for entry in result
        ]
        response_dict['search_time'] = datetime.now() - start_time

    return render_to_response('main.html', response_dict)

def servers_page(request):
    '''Page with list of scanned servers'''
    active_only = request.method == 'GET' and 'active' in request.GET
    servers = get_servers(active_only)
    return render_to_response('servers.html', {'servers': servers})
