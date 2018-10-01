#!/usr/bin/env python3
# coding: utf-8


""" Download models used across app """

import threading
import traceback

from pymongo import MongoClient

from statsf1.logger import get_logger, log_race


class DownloadThread(threading.Thread):
    def __init__(self, queue, local_db):
        super(DownloadThread, self).__init__()

        self.queue = queue
        self.local_db = local_db
        self.daemon = True
        self.logger = get_logger()

    def save_to_db(self, race):
        client = MongoClient()  # get instance of MongoDB
        db = client[self.local_db]  # get db

        collection = db[race.year]  # 1 collection per year
        collection.insert_one(race.to_dict())

        client.close()

    def run(self):
        while True:
            race = self.queue.get()

            try:
                race.parse()

                self.save_to_db(race)
                log_race(race)
            except:
                tb = traceback.format_exc()
                self.logger.error(race.url)
                self.logger.error(tb)

            self.queue.task_done()
