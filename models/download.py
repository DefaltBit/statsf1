#!/usr/bin/env python3
# coding: utf-8


""" Creates local database and downloads data """

from queue import Queue

from pymongo import MongoClient

from statsf1.logger import log_races
from statsf1.models.core import DownloadThread
from statsf1.models.statsf1 import StatF1

N_THREADS = 8  # threads to use when downloading


def get_all_races():
    driver = StatF1()
    return driver.get_all_races()


def clean_db(db_name):
    client = MongoClient()  # mongodb client
    client.drop_database(db_name)  # remove all previous data
    client.close()  # flush and close


def download(local_db):
    clean_db(local_db)
    races = get_all_races()
    log_races(races)

    queue = Queue()
    for race in races:
        queue.put(race)

    for i in range(N_THREADS):
        t = DownloadThread(queue, local_db)
        t.start()

    queue.join()
