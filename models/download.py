#!/usr/bin/env python3
# coding: utf-8


""" Creates local database and downloads data """

import asyncio

from pymongo import MongoClient

from statsf1.models.core import DownloadThread
from statsf1.models.statsf1 import StatF1

N_THREADS = 8  # threads to use when downloading
DATABASE_NAME = "statsf1"  # name of mongodb database to use
MONGODB_CLIENT = MongoClient()  # mongodb client
MONGODB_CLIENT.drop_database(DATABASE_NAME)  # remove all previous data
DATABASE = MONGODB_CLIENT[
    DATABASE_NAME
]  # database to use
for coll in DATABASE.collection_names():
    DATABASE[coll].create_index("num", unique=True)  # set primary key


def get_all_races():
    driver = StatF1()
    return driver.get_all_races()


def download(local_db):
    races = get_all_races()
    queue = asyncio.Queue()
    for url in races:
        queue.put(url)

    for i in range(N_THREADS):
        t = DownloadThread(queue, local_db)
        t.start()

    queue.join()
