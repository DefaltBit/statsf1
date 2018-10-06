#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """
from statsf1.explore.models import Explorer

from statsf1.stats.models import WeekendStats


# todo
# regr
#  http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
# clf
#  http://scikit-learn.org/stable/auto_examples/classification/plot_classification_probability.html


class PredictExplore:
    def __init__(self, db, years, year, weekend):
        self.stats = WeekendStats(db, years, weekend)
        self.weekend = Explorer.get_weekend_collection(weekend)
        self.year = Explorer.get_year_collection(year)

    @staticmethod
    def _preprocess(data):
        pass

    @staticmethod
    def _postprocess(data):
        pass

        # todo
        # static methods (parse, get valid weekends ...)


class DriverPredict(PredictExplore):
    def __init__(self, db, driver, years, year, weekend):
        super().__init__(db, years, year, weekend)
        self.driver = str(driver)

    def get_race_winner(self):
        pass  # todo

    def get_race_podium(self):
        pass  # todo

    def get_completes_race(self):
        pass  # todo

    def get_q_winner(self):
        pass  # todo

    def get_best_lap_winner(self):
        pass  # todo


class ChassisPredict(PredictExplore):
    # all true false -> 0, 1 -> clf (and also show prob)
    def __init__(self, db, chassis, years, year, weekend):
        super().__init__(db, years, year, weekend)
        self.chassis = str(chassis)

    def get_race_winner(self):
        pass  # todo

    def get_both_points(self):
        pass  # todo

    def get_both_complete_race(self):
        pass  # todo

    def get_q_winner(self):
        pass  # todo


class WeekendPredict(PredictExplore):
    # all regr

    def get_n_drivers_finishes(self):
        pass  # todo

    def get_q_position_of_winner(self):
        pass  # todo

    def get_race_win_margin(self):
        pass  # todo

    def get_q_win_margin(self):
        pass  # todo

    def get_grand_chelem(self):
        pass  # todo
        #  will there be ? | true false -> 0, 1 -> clf (and also show prob)
