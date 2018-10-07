#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """
# todo
# predict based on other drivers/chassis positions
# test predictions on past data (to see which params are best)
# class to get prob / get pred on data

import abc

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC

from statsf1.explore.models import ByYearExplorer, WeekendExplorer
from statsf1.stats.models import WeekendStats, WeekendsStats
from tools.logger import log_matrix, log_ml_algorithm


def just_these_columns(df, columns):
    columns_to_drop = [
        column
        for column in df.keys()
        if column not in columns
    ]
    return df.drop(columns_to_drop, axis=1)  # columns


def just_common_columns(dfs):
    common_columns = list(dfs[0].keys())
    for df in dfs[1:]:
        common_columns = list(set(common_columns).intersection(df.keys()))

    return [
        just_these_columns(df, common_columns)
        for df in dfs
    ]


class MlAlgorithm:
    def __init__(self, alg):
        self.alg = alg

    def _train(self, x_train, y_train):
        y_train = y_train.ix[:, 0]  # first column
        self.alg.fit(x_train, y_train)

    def _predict(self, x_pred):
        return self.alg.predict(x_pred)

    def make_prediction(self, x_train, y_train, x_pred):
        self._train(x_train, y_train)

        log_ml_algorithm(self.alg)
        return self._predict(x_pred)

    @staticmethod
    @abc.abstractmethod
    def get_default():
        return None


class RegrAlgorithm(MlAlgorithm):
    def get_coefficients(self):
        return []  # todo

    @staticmethod
    def get_default():
        alg = RandomForestRegressor(max_depth=2, n_estimators=10)
        return RegrAlgorithm(alg)


class ClfAlgorithm(MlAlgorithm):
    def get_probabilities(self, x_pred):
        return self.alg.predict_proba(x_pred)  # class probability

    @staticmethod
    def get_default():
        alg = SVC(kernel='linear', C=10, probability=True)
        return ClfAlgorithm(alg)


class PredictExplore:
    def __init__(self, db, years, year, weekend):
        self.weekend = weekend

        years = sorted(set(list(years) + [year]))
        self.weekend_stats = WeekendStats(db, years, weekend)

        year_explorer = ByYearExplorer(db, year)
        weekends = year_explorer.get_names()  # weekends of this year
        self.stats = WeekendsStats(db, years, weekends)

        self.regr = RegrAlgorithm.get_default()  # ml algorithms
        self.clf = ClfAlgorithm.get_default()

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

        years_to_drop = x_train.index[:n_years]  # there will be NaN
        x_train = x_train.drop(years_to_drop)
        y_train = y_train.drop(years_to_drop)

        # remove year column
        x_years = x_train[WeekendExplorer.YEAR_KEY].tolist()  # years
        x_train = x_train.drop([WeekendExplorer.YEAR_KEY], axis=1)
        y_train = y_train.drop([WeekendExplorer.YEAR_KEY], axis=1)
        x_predict_years = x_predict[WeekendExplorer.YEAR_KEY].tolist()  # years
        x_predict = x_predict.drop([WeekendExplorer.YEAR_KEY], axis=1)

        # drop NaN
        x_train = x_train.dropna(axis=1)  # remove weekends not in all years
        y_train = y_train.dropna(axis=1)
        x_predict = x_predict.dropna(axis=1)

        # only common weekends between X train and X pred (past years and this)
        [x_train, x_predict] = just_common_columns([x_train, x_predict])

        # debug data
        log_matrix("X train", x_train, row_names=x_years, show_values=True)
        log_matrix("Y train", y_train, row_names=x_years, show_values=True)
        log_matrix("X predict (transpose)", x_predict,
                   row_names=x_predict_years, show_values=True)

        return x_train, y_train, x_predict

    @staticmethod
    def get_prediction(alg, x_train, y_train, x_pred):
        pred = alg.make_prediction(x_train, y_train, x_pred)
        return pred[0]  # just 1 sample -> so first value

    def get_regr_prediction(self, x_train, y_train, x_pred):
        return self.get_prediction(self.regr, x_train, y_train, x_pred)

    def get_clf_prediction(self, x_train, y_train, x_pred):
        return self.get_prediction(self.clf, x_train, y_train, x_pred)

    def predict_regr(self, data, n_years):
        x_train, y_train, x_predict = self._pre_process(data, n_years=n_years)
        return self.get_regr_prediction(x_train, y_train, x_predict)

    def predict_clf(self, data, n_years):
        x_train, y_train, x_predict = self._pre_process(data, n_years=n_years)
        return self.get_clf_prediction(x_train, y_train, x_predict)


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
    def get_n_drivers_finishes(self):
        data = self.stats.get_race_finishes()
        n_years = 1

        regr = self.predict_regr(data, n_years)
        clf = None  # self.predict_clf(data, n_years)

        return regr, clf

    def get_race_winner_q_position(self):
        data = self.stats.get_race_winner_q_position()
        n_years = 3

        regr = self.predict_regr(data, n_years)
        clf = self.predict_clf(data, n_years)

        return regr, clf

    def get_race_win_margin(self):
        data = self.stats.get_race_win_margin()
        n_years = 3

        regr = self.predict_regr(data, n_years)
        # todo clf by classes in stats.json

        return regr

    def get_q_win_margin(self):
        data = self.stats.get_q_win_margin()
        n_years = 3

        regr = self.predict_regr(data, n_years)
        # todo clf by classes in stats.json

        return regr

    def get_grand_chelem(self):
        pass  # todo
        #  will there be ? | true false -> 0, 1 -> clf (and also show prob)
