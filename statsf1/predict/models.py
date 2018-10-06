#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

import pandas as pd

from statsf1.explore.models import ByYearExplorer, SummaryExplorer, \
    WeekendExplorer
from statsf1.stats.models import WeekendStats


# todo
# regr
#  http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
# clf
#  http://scikit-learn.org/stable/auto_examples/classification/plot_classification_probability.html

# todo
# predict based on other drivers/chassis positions

class PredictExplore:
    def __init__(self, db, years, year, weekend):
        self.weekend = weekend

        years = list(years) + [year]
        self.stats = WeekendStats(db, years, weekend)

        year_explorer = ByYearExplorer(db, year)
        weekends = year_explorer.get_names()  # weekends of this year
        self.past_explorer = SummaryExplorer(db, years, weekends)

    def _pre_process(self, data, n_years=0):
        """
        :param data: pd.DataFrame
            Rows are years, columns are weekends, cells are value of weekend
            in year
        :param n_years: int
            In train data, add also data about last n years
        :return: tuple (pd.DataFrame, pd.DataFrame, pd.DataFrame)
            X train (values of past year), Y train (results of values based
            on past year), X predict (values of this year)
        """

        labels = list(data.keys())
        labels.remove(self.weekend)

        x_labels = labels
        x_data = data[x_labels]
        x_df = pd.DataFrame(data=x_data, columns=x_labels)

        predictions_row = x_df.shape[0] - 1  # last row

        x_predict = x_df.iloc[predictions_row]
        x_predict = pd.DataFrame(data=[x_predict.tolist()], columns=x_labels)
        x_train = x_df.drop([predictions_row])

        y_labels = [WeekendExplorer.YEAR_KEY, self.weekend]
        y_data = data[y_labels]
        y_df = pd.DataFrame(data=y_data, columns=y_labels)
        y_train = y_df.drop([predictions_row])

        if n_years > 0:
            y_past = y_train.copy()
            y_past[self.weekend] = y_past[self.weekend].shift(1)  # shift

            for year in range(n_years):
                year_label = self.weekend + " - " + str(year + 1)
                x_labels += [year_label]
                x_train[year_label] = y_past[self.weekend]

                row = y_past.shape[0] - 1 - year
                x_predict[year_label] = [y_train.iloc[row, 1]]
                y_past[self.weekend] = y_past[self.weekend].shift(1)  # shift

        return x_train, y_train, x_predict

    @staticmethod
    def _post_process(data):
        pass  # todo

    def _get_clf(self):
        pass  # todo

    def _get_regr(self):
        pass  # todo


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
    # true false -> 0, 1 -> clf (and also show prob)
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
    # regr
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
