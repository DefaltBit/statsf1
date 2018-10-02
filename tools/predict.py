#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """
from statsf1.tools.stats import Statistician


class Predictor:
    def __init__(self, race, year, db, n_years):
        self.stats = Statistician(race, year, db, n_years)

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


def run(race, driver, year, n_years, n_drivers, db):
    pred = Predictor(race, year, db, n_years)
