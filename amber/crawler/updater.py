# -*- coding: utf-8 -*-
'''Updating server data'''
from multiprocessing import Process, Pipe
from ..mongo_db import MDB
from .samba import scan_host
from .writer import writer
from .postprocessor import postprocessing
from .servers import get_server_id, update_server_info
from datetime import datetime
import logging

logging.basicConfig(level = logging.INFO)

def update_host(host, index_path=None, auto_name=False, name=None):
    '''Updates given host'''
    scan_start = datetime.now()

    logging.info('Started scanning host ' + host)

    server_id = get_server_id(host, auto_name, name)

    logging.info('Starting scanner and writer')

    # Пайп для передачи данных от сканера к записывателю данных
    output_pipe, input_pipe = Pipe(False)

    # Коллекция для временного хранения результатов
    tmp_collection = MDB['tmp.' + server_id]
    tmp_collection.drop()

    # Запускаем сканер и записыватель
    writer_proc = Process(target=writer, args=(output_pipe, tmp_collection))
    writer_proc.start()

    is_scan_ok = scan_host(host, index_path, input_pipe)

    writer_proc.join()


    # Запускаем обработку полученных данных и их слитие в основную коллекцию
    if is_scan_ok:
        postprocessing(server_id, tmp_collection, scan_start)
    else:
        logging.info('Failed to scan host')

    tmp_collection.drop()


    # Обновляем информацию по серверу
    update_server_info(server_id, {
        'is_active': is_scan_ok,
        'scan_start': scan_start,
        'scan_end': datetime.now(),
    })

    logging.info('Finished')
