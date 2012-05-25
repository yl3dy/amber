# -*- coding: utf-8 -*-
from multiprocessing import Process, Pipe
from ..mongo_db import mdb, servers_collection
from samba import scan_host
from writer import writer
from datetime import datetime
from postprocessor import postprocessing
import logging

logging.basicConfig(level = logging.INFO)

def update_host(host):
    scan_start = datetime.now()

    logging.info('Started scanning host ' + host)

    server = servers_collection.find_one({'host': host})
    #TODO Сделать выставление коротких айдишников
    if server == None:
        server_id = str(servers_collection.save({'host': host}))
        server = servers_collection.find_one({'host': host})
    else:
        server_id = str(server['_id'])

    logging.info('Starting scanner and writer')

    # Пайп для передачи данных от сканера к записывателю данных
    output_pipe, input_pipe = Pipe(False)

    # Коллекция для временного хранения результатов
    tmp_collection = mdb['tmp.' + server_id]
    tmp_collection.drop()

    # Запускаем сканер и записыватель
    writer_proc = Process(target=writer, args=(output_pipe, tmp_collection))
    writer_proc.start()

    is_scan_ok = scan_host(host, input_pipe)

    writer_proc.join()

    

    # Запускаем обработку полученных данных и их слитие в основную коллекцию
    if is_scan_ok:
        postprocessing(server_id, tmp_collection, scan_start)
    else:
        logging.info('Failed to scan host')

    tmp_collection.drop()


    logging.debug('Updating server info')
    # Обновляем информацию по серверу
    server['scan_start'] = scan_start
    server['is_active'] = is_scan_ok
    server['scan_end'] = datetime.now()
    servers_collection.save(server)

    logging.info('Finished')
