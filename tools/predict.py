#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from statsf1.tools.explorer import RaceExplorer

RACE_COMPLETED_FORMAT = ""


class Predictor:
    def __init__(self, race, year, db):
        self.explorer = RaceExplorer(race, year, db)

    def get_race_completed(self, n_years):
        labels, summaries = self.explorer.get_previous_years_result(n_years)

        race_completed = {
            year: len([
                row[4]
                for row in data
                if row[4] == "yes"
            ])
            for year, data in summaries.items()
        }


def run(db):
    driver = Predictor("Japon", 2018, db)
    result = driver.get_race_completed(10)
    print(RACE_COMPLETED_FORMAT.format(result))
