# -*- coding: utf-8 -*-
from multiprocessing import Process, Pipe
from ..mongo_db import mdb
from samba import scan_host
from writer import writer
from datetime import datetime
from postprocessor import postprocessing
from servers import get_server_id, update_server_info
import logging

logging.basicConfig(level = logging.INFO)

def update_host(host):
    scan_start = datetime.now()

    logging.info('Started scanning host ' + host)

    server_id = get_server_id(host)

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


    # Обновляем информацию по серверу
    update_server_info(server_id, {
        'scan_start': scan_start,
        'is_active': is_scan_ok,
        'scan_end': datetime.now(),
    })

    logging.info('Finished')
