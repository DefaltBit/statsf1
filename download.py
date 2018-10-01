#!/usr/bin/env python3
# coding: utf-8


""" Creates local database and downloads data """

from pymongo import MongoClient

from statsf1.models.download import Downloader
from statsf1.models.statsf1 import StatF1

N_THREADS = 8  # threads to use when downloading


def get_races():
    driver = StatF1()
    return driver.get_all_races()


def clean_db(db_name):
    client = MongoClient()  # mongodb client
    client.drop_database(db_name)  # remove all previous data
    client.close()  # flush and close


def download(local_db):
    clean_db(local_db)
    races = get_races()
    Downloader(races, local_db).run()
