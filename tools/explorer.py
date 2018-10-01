#!/usr/bin/env python3
# coding: utf-8


""" Explore database """

from hal.mongodb.utils import get_documents_count, get_documents_in_database

DATABASE_NAME = "statsf1"  # name of mongodb database to use


def count_races(db):
    return get_documents_count(db)


def average_race_entrants(db):
    races = get_documents_in_database(db)
    race_entrants = 0
    key = "race_entrants"

    for race in races:
        if key in race:
            data = race[key]
            race_entrants += len(data["Pilote "])

    return race_entrants / len(races)


def run():
    tot_races = count_races(DATABASE_NAME)
    average_drivers = average_race_entrants(DATABASE_NAME)
    tot_entries = tot_races * 4 * average_drivers

    message = "{} races and on average {:.2f} drivers -> {} total entries"
    print(message.format(tot_races, average_drivers, tot_entries))
