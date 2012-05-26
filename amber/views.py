# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from mongo_db import mdb, main_collection, servers_collection, split_words
from django.conf import settings
from datetime import datetime
import os

RESULT_NUM = 100

ENTRY_TYPES = {
    'folders': {'title': 'Папки', 'is_file': False},
    'files': {'title': 'Файлы', 'is_file': True},
    'video': {'title': 'Видео', 'extensions': ['mp4', 'avi', '3gp', 'rmvb', 'wmv', 'mkv', 'mpg', 'mov', 'vob', 'flv', 'swf', 'ogm']},
    'music': {'title': 'Музыка', 'extensions': ['mp3', 'wma', 'flac', 'aac', 'mmf', 'amr', 'm4a', 'm4r', 'ogg', 'mp2', 'wav']},
    'pictures': {'title': 'Изображения', 'extensions': ['jpg', 'jpeg', 'png', 'ico', 'bmp', 'gif', 'tif', 'tiff', 'pcx', 'tga', 'nef']},
    'books': {'title': 'Книги', 'extensions': ['djvu', 'pdf', 'epub', 'fb2', 'html', 'htm', 'txt', 'ps', 'doc', 'rtf']},
}

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

def get_paths(servers, paths, is_orthodox):
    res = []
    if is_orthodox:
        form_url = lambda host, path: 'smb://' + host + path
    else:
        form_url = lambda host, path: 'file:////' + host + path
    for server_id in paths:
        server = servers[server_id]
        for path in paths[server_id]:
            res.append((
                server['is_active'],
                form_url(server['host'], path),
                server['name'] + path if 'name' in server else server['host'] + path,
            ))
    return res

def get_servers():
    res = {}
    for server in servers_collection.find(): res[str(server['_id'])] = server
    return res

def postprocess_entry(servers, entry, is_orthodox):
    return {
        'name': entry['n'],
        'size': sizeof_fmt(entry['s']),
        'paths': get_paths(servers, entry['p'], is_orthodox),
        'is_file': entry['f'],
    }

def postprocess_results(servers, results, is_orthodox):
    return [postprocess_entry(servers, entry, is_orthodox) for entry in results]

def get_entry_type_query(entry_type):
    if entry_type not in ENTRY_TYPES: return {}
    entry_filter = ENTRY_TYPES[entry_type]
    if 'is_file' in entry_filter: return {'f': entry_filter['is_file']}
    elif 'extensions' in entry_filter: return {'e': {'$in': entry_filter['extensions']}}
    return {}

def mainpage(request):
    servers = get_servers()
    response_dict = {
        'servers': servers,
        'entry_types': ENTRY_TYPES,
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

        t = datetime.now()

        # Basic search through name, type and server
        search_dict = {'w': {'$all': split_words(search_string)}}
        if server_request: search_dict['p.' + server_request] = {'$exists': True}
        if entry_type: search_dict.update(get_entry_type_query(entry_type))
        result = main_collection.find(search_dict)

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
        result = result.limit(RESULT_NUM)

        # Looking into performance help if debugging
        #if settings.DEBUG: response_dict['performance'] = result.explain() 

        response_dict['search_result'] = postprocess_results(servers, result, is_orthodox)
        response_dict['search_time'] = datetime.now() - t

    return render_to_response('main.html', response_dict)

def servers(request):
    return render_to_response('servers.html', {'servers': get_servers()})
