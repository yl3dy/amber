from multiprocessing import Process, Pipe
from ..mongo_db import servers_collection
from samba import scan_host
from writer import writer
from datetime import datetime

def update_host(host):
    scan_start = datetime.now()

    server = servers_collection.find_one({'host': host})
    if server == None:
        server_id = str(servers_collection.save({'host': host}))
        server = servers_collection.find_one({'host': host})
    else:
        server_id = str(server['_id'])

    output_pipe, input_pipe = Pipe(False)


    writer_proc = Process(target=writer, args=(output_pipe, server_id))
    writer_proc.start()

    is_scan_ok = scan_host(host, input_pipe)

    writer_proc.join()

    server['scan_start'] = scan_start
    server['is_active'] = is_scan_ok
    server['scan_end'] = datetime.now()
    servers_collection.save(server)
