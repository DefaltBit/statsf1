#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from statsf1.stats.models import WeekendStats


# todo
# regr
#  http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
# clf
#  http://scikit-learn.org/stable/auto_examples/classification/plot_classification_probability.html


class PredictExplore:
    @staticmethod
    def _preprocess(data):
        pass

    @staticmethod
    def _postprocess(data):
        pass

        # todo
        # static methods (parse, get valid weekends ...)


class DriverPredict(PredictExplore):
    def __init__(self, db, driver, years, weekend):
        self.driver = str(driver)
        self.stats = WeekendStats(db, years, weekend)

        # todo predict
        # -- Race
        # winner ?
        # podium ?
        # completes race ?
        # -- Q
        # win ?
        # -- Best lap
        # win ?


class ChassisPredict(PredictExplore):
    def __init__(self, db, chassis, years, weekend):
        self.chassis = str(chassis)
        self.stats = WeekendStats(db, years, weekend)

        # todo predict
        # -- Race
        # winner ?
        # both points (top 10) ? | true false -> 0, 1 -> clf (and also show prob)
        # both complete race ? | true false -> 0, 1 -> clf (and also show prob)
        # -- Q
        # win ? | true false -> 0, 1 -> clf (and also show prob)


class WeekendPredict(PredictExplore):
    def __init__(self, db, years, weekend):
        self.stats = WeekendStats(db, years, weekend)

        # todo predict
        # -- Race
        # # drivers finishes | regr
        # Q position of winner | regr
        # win margin | regr
        # -- Q
        # win margin | regr
        # -- Grand chelem
        # will there be ? | true false -> 0, 1 -> clf (and also show prob)
