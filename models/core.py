#!/usr/bin/env python3
# coding: utf-8


""" Download models used across app """

import logging
import threading

from pymongo import MongoClient

LOGGER = logging.getLogger("statsf1")
LOGGER.setLevel(logging.DEBUG)
LOG_PRINT_FORMAT = "thread-{%d}: {} from {}"


class DownloadThread(threading.Thread):
    def __init__(self, queue, local_db):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.local_db = local_db
        self.daemon = True

    def save_to_db(self, race):
        client = MongoClient()  # get instance of MongoDB
        db = client[self.local_db]  # get db
        collection = db[race.year]  # 1 collection per year
        collection.insert_one(race.to_dict())

    def log(self, race):
        thread_id = threading.current_thread().ident
        LOGGER.info(LOG_PRINT_FORMAT.format(thread_id, race.text, race.year))

    def run(self):
        while True:
            try:
                race = self.queue.get()
                race.parse()

                self.save_to_db(race)
                self.log(race)
            except Exception as e:
                print(e)

            self.queue.task_done()
