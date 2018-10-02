#!/usr/bin/env python3
# coding: utf-8


""" Explore database """

from hal.mongodb.utils import get_documents_count, get_documents_in_database
from hal.streams.pretty_table import pretty_format_table
from pymongo import MongoClient

from statsf1.tools.utils import DNF, pretty_time, parse_time, NUM_FORMAT


class Explorer:
    def __init__(self, db):
        self.db_name = db
        self.client = MongoClient()  # mongodb client
        self.db = self.client[self.db_name]

    def count_races(self):
        return get_documents_count(self.db_name)

    def average_race_entrants(self):
        races = get_documents_in_database(self.db_name)
        race_entrants = 0
        key = "race_entrants"

        for race in races:
            if key in race:
                data = race[key]
                race_entrants += len(data["Pilote "])

        return race_entrants / len(races)

    def get_races(self, year):
        collection = self.db[year]
        return [
            race
            for race in collection.find()
        ]


class RaceExplorer(Explorer):
    RACE_SUMMARY_LABELS = ["race pos", "driver", "chassis",
                           "race laps", "race completed?", "race time",
                           "Q pos", "Q time", "race VS Q",
                           "best lap pos", "best lap", "best lap VS Q"]
    DRIVER_SUMMARY_LABELS = ["year", "race pos", "chassis",
                             "race laps", "race completed?", "race time",
                             "Q pos", "Q time", "race VS Q",
                             "best lap pos", "best lap", "best lap VS Q"]

    def __init__(self, race, year, db):
        Explorer.__init__(self, db)

        self.raw_race = str(race)
        self.raw_year = str(year)
        self.race = None

    def get_race(self):
        if self.race is None:
            collection = self.db[self.raw_year]
            race = [
                race
                for race in collection.find()
                if race["name"] == self.raw_race
            ]

            if race:
                return race[0]

        return self.race

    def get_drivers_summary(self, key, labels):
        race = self.get_race()
        drivers = race[key]["Pilote "]  # drivers are main key
        data = [
            race[key][label]
            for label in labels
        ]  # find all other data

        data = {
            driver: {
                label: data[j][i]
                for j, label in enumerate(labels)
            }
            for i, driver in enumerate(drivers)
        }

        for driver, labels in data.items():
            if "Pos " in labels:
                try:
                    int(data[driver]["Pos "])  # fix null positions
                except:
                    data[driver]["Pos "] = "ab"

        return data

    def get_drivers(self):
        race = self.get_race()
        return race["result"]["Pilote "]

    def get_race_summary(self):
        return self.get_drivers_summary(
            "result",
            ["Ch\\xc3\\xa2ssis ", "Pos ", "Tour ", "\xa0"]
        )

    def get_qualification_summary(self):
        return self.get_drivers_summary(
            "qualifications",
            ["Ch\\xc3\\xa2ssis ", "Pos ", "Temps "]
        )

    def get_best_laps_summary(self):
        return self.get_drivers_summary(
            "best_laps",
            ["Ch\\xc3\\xa2ssis ", "n ", "Temps "]
        )

    def get_summary(self):
        race = self.get_race_summary()
        qualification = self.get_qualification_summary()
        best_laps = self.get_best_laps_summary()

        standings = sorted(race.items(), key=lambda x: int(x[1]["Pos "], 16))
        race_laps = float(race[standings[0][0]]["Tour "])  # laps of the winner
        summary = []

        for driver, _ in standings:
            race_pos = race[driver]["Pos "]
            try:
                int(race_pos)
            except:
                race_pos = DNF

            try:
                race_completed = int(race[driver]["Tour "]) > 0.9 * race_laps
            except:
                race_completed = False

            if race_completed:
                race_completed = "yes"
            else:
                race_completed = "no"

            try:
                race_time = race[driver]["\xa0"].split("(")[0].strip()
            except:
                race_time = DNF

            row = [
                race_pos, driver, race[driver]["Ch\\xc3\\xa2ssis "],
                race[driver]["Tour "], race_completed, race_time
            ]

            try:
                q_pos = qualification[driver]["Pos "]
                q_lap = pretty_time(qualification[driver]["Temps "])
                q_lap_time = parse_time(q_lap)

                try:
                    race_vs_q = str(int(race_pos) - int(q_pos))
                except:
                    race_vs_q = DNF
            except:
                q_pos = DNF
                q_lap = DNF
                q_lap_time = 0
                race_vs_q = DNF

            row += [q_pos, q_lap, race_vs_q]

            try:
                best_lap_pos = best_laps[driver]["n "]
                best_lap = pretty_time(best_laps[driver]["Temps "])
                best_lap_time = parse_time(best_lap)
                ratio_best_q = 100.0 * (best_lap_time / q_lap_time - 1)
                ratio_best_q = NUM_FORMAT.format(ratio_best_q) + "%"
            except:
                best_lap_pos = DNF
                best_lap = DNF
                ratio_best_q = DNF

            row += [best_lap_pos, best_lap, ratio_best_q]
            summary.append(row)

        return self.RACE_SUMMARY_LABELS, summary

    def get_previous_years_result(self, n_years):
        year = int(self.raw_year)
        years = range(year - n_years + 1, year + 1)

        return self.RACE_SUMMARY_LABELS, {
            str(year):
                RaceExplorer(
                    self.raw_race, str(year), self.db_name
                ).get_summary()[1]
            for year in years
        }

    def get_previous_years_summary(self, n_years, driver):
        labels, summaries = self.get_previous_years_result(n_years)
        data = {
            year: [row for row in table if row[1] == driver]
            for year, table in summaries.items()
        }
        data = {
            year: row[0] if row else [DNF] * len(labels)
            for year, row in data.items()
        }

        table = [
            [year] + [row[0]] + row[2:]  # remove driver column
            for year, row in data.items()
        ]
        table = list(reversed(table))  # from nearest result to oldest

        return self.DRIVER_SUMMARY_LABELS, table


def print_averages(db):
    driver = Explorer(db)
    tot_races = driver.count_races()
    average_drivers = driver.average_race_entrants()
    tot_entries = tot_races * 4 * average_drivers

    message = "{} races and on average {:.2f} drivers -> {} total entries"
    print(message.format(tot_races, average_drivers, tot_entries))


def print_available_races(db, year):
    driver = Explorer(db)
    races = driver.get_races(str(year))
    races = sorted([
        race["name"]
        for race in races
    ])
    print(races)


def run(db):
    driver = RaceExplorer("Japon", 2011, db)
    labels, summary = driver.get_summary()
    print(pretty_format_table(labels, summary))
