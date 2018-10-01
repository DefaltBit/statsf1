#!/usr/bin/env python3
# coding: utf-8


""" Creates local database and downloads data """

from pymongo import MongoClient

from statsf1.models.download import Downloader
from statsf1.models.statsf1 import StatF1


def get_races(year):
    driver = StatF1()
    return driver.get_races(year)


def clean_db(year, db_name):
    client = MongoClient()  # mongodb client
    db = client[db_name]
    db[year].delete_many({})  # remove all previous data
    client.close()  # flush and close


def update(year, local_db):
    clean_db(year, local_db)
    races = get_races(year)
    Downloader(races, local_db).run()
