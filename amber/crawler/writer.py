'''Handeling writing results of scanning into the collection'''
import hashlib, os, logging
from bson import binary

def get_name(path):
    '''Returns name of file or folder by path'''
    return os.path.split(path)[1]

def get_unic_id(data):
    '''Returns identificator for entry'''
    unic_str = u':'.join([
        get_name(data['path']),
        str(data['size']),
        data['change_time'].isoformat(),
        str(data['is_file']),
    ])
    # pylint: disable-msg=E1101
    bin_string = hashlib.md5(unic_str.encode('utf8')).digest()
    return binary.Binary(bin_string, binary.MD5_SUBTYPE)

def writer(output_pipe, collection):
    '''Writing formatted data from pipe into collection'''
    logging.debug('Started writer')
    while True:
        data = output_pipe.recv()

        if data == None:
            break

        path = data['path']
        data['_id'] = get_unic_id(data)
        data['name'] = get_name(path)
        del data['path']

        if not data['is_file']:
            path += '/'

        collection.update(data, {'$addToSet': {'paths': path}}, upsert=True)
