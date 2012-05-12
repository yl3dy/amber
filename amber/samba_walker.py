#!/usr/bin/python2
import smbc

# smbc entry types
SMBC_FILE = 8L
SMBC_DIR = 7L
SMBC_SERVICE = 3L

def smb_walk(host):
    """ Generator to walk around SMB tree """

    smb_host = 'smb://' + host
    ctx = smbc.Context()
    cache = [ [], ]
    item_type = lambda entry: 'file' if entry.smbc_type == SMBC_FILE else 'dir'

    def get_return_object(entry):
        path = entry[0]
        tp = entry[1]
        data =  {
            'path': path.replace(smb_host, '').decode('utf8'),
            'type': tp,
        }
        # TODO Add detecting file meta information
        if tp == 'file':
            fstat = ctx.open(path).fstat()
            data['fstat'] = fstat
        return data

    # initial filling of cache
    for item in ctx.opendir(smb_host).getdents():
        if item.smbc_type == SMBC_SERVICE:
            cache[0].append((smb_host + '/' + item.name, item_type(item)))
    while cache != []:
        item = cache[-1].pop()
        yield get_return_object(item)

        if item[1] == 'dir':
            try:
                tmp = []
                for entry in ctx.opendir(item[0]).getdents():
                    if entry.name not in ['..', '.']:
                        tmp.append((item[0] + '/' + entry.name, item_type(entry)))
                cache.append(tmp)
            except smbc.PermissionError:
                pass
            except smbc.NoEntryError:
                print('Can\'t read entry named '+item[0])
            except:
                print('Random fail has happened on entry '+item[0]+' which is '+item[1])

        # Removing empty elements
        while cache and cache[-1] == []: cache.pop()

