from ..mongo_db import servers_collection
import base64, struct, logging

def encode64(n):
  data = struct.pack('<Q', n).rstrip('\x00')
  if len(data)==0:
    data = '\x00'
  s = base64.urlsafe_b64encode(data).rstrip('=')
  return s
 
def decode64(s):
  data = base64.urlsafe_b64decode(str(s) + '==')
  n = struct.unpack('<Q', data + '\x00'* (8-len(data)) )
  return n[0]

def get_new_id():
    int_ids = [decode64(server['_id']) for server in servers_collection.find()]
    if not int_ids: return encode64(0)
    int_ids.sort()
    return encode64(int_ids[-1] + 1)



def get_server_id(host):
    logging.info('Getting server id')
    server = servers_collection.find_one({'host': host})
    if server == None:
        server_id = get_new_id()
        logging.info('Creating new server with host %s and id %s' % (host, server_id))
        servers_collection.save({
            '_id': server_id,
            'name': host,
            'host': host,
            'is_active': False,
            'scan_start': None,
            'scan_end': None,
        })
    else:
        server_id = server['_id']
    return server_id

def update_server_info(server_id, data):
    logging.info('Updating server info')
    servers_collection.update({'_id': server_id}, {'$set': data})
