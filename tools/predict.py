#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from hal.data.lists import find_commons
from hal.data.matrix import Matrix

from statsf1.tools.explorer import RaceExplorer
from statsf1.tools.stats import Statistician
from statsf1.tools.utils import DNF


class Predictor:
    def __init__(self, race, year, db, n_years):
        self.stats = Statistician(race, year, db, n_years)
        self.explorer = self.stats.explorer

    def _get_year_results(self, label, year):
        names, races = RaceExplorer.get_year_results(
            year, self.explorer.db_name
        )
        results = [
            race[1]  # first element are the labels
            for race in races
        ]
        labels = races[0][0]
        column = labels.index(label)  # find which column to get

        label_results = [
            Matrix(race).get_column(column)
            for race in results
            if race[0][1] != DNF  # discard DNFs races
        ]
        return {
            name: result
            for name, result in zip(names, label_results)
        }  # race name -> race result

    def _get_races_matrix(self, label):
        max_year = int(self.explorer.raw_year) + 1  # including this year
        min_year = max_year - self.stats.n_years
        years = range(min_year, max_year)  # years to get
        results = {
            str(year): self._get_year_results(label, str(year))
            for year in years
        }  # all races results across all years

        races = find_commons([
            list(results.keys())  # result keys are the name of the races
            for year, results in results.items()
        ])  # races in common between years
        results = {
            year: {
                race: data
                for race, data in results.items() if race in races
            }
            for year, results in results.items()
        }

        return results

    def _get_race_chassis_win(self):
        return None  # todo

    def print_race_chassis_win(self):
        pass  # todo

    def _get_race_driver_win(self):
        return None  # todo

    def print_race_driver_win(self):
        pass  # todo

    def _get_q_driver_win(self):
        return None  # todo

    def print_q_driver_win(self):
        pass  # todo

    def _get_q_chassis_win(self):
        return None  # todo

    def print_q_chassis_win(self):
        pass  # todo

    def _get_podium(self):
        return None  # todo

    def print_podium(self):
        pass  # todo

    def _get_chassis_complete(self):
        return None  # todo

    def print_chassis_complete(self):
        pass  # todo

    def _get_grand_chelem(self):
        return None  # todo

    def print_grand_chelem(self):
        pass  # todo


def run(race, driver, year, n_years, n_drivers, db):
    pred = Predictor(race, year, db, n_years)

    x = pred._get_races_matrix("driver")
    for year, races in x.items():
        print(races.keys())  # check are in same order
