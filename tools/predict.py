#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from statsf1.tools.stats import Statistician


class Predictor:
    def __init__(self, race, year, db, n_years):
        self.stats = Statistician(race, year, db, n_years)
        self.explorer = self.stats.explorer

    def _get_races_matrix(self, label):
        max_year = int(self.explorer.raw_year)
        min_year = max_year - self.stats.n_years
        years = range(min_year, max_year + 1)  # years to get
        races = [
            self.explorer.get_races(year)
            for year in years
        ]  # all races across all years
        unique_races = set(sum(races, []))  # just unique races
        races = [
            [race for race in year_races if race in unique_races]
            for year_races in races
        ]

        summaries = {
            str(year): []
            for year in years
        }

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
