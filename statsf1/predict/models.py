#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """
# todo
# predict based on other drivers/chassis positions

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC

from statsf1.explore.models import ByYearExplorer, WeekendExplorer
from statsf1.stats.models import WeekendStats, WeekendsStats
from tools.logger import log_matrix


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


# todo
class MlPredictor:
    def __init__(self, alg):
        self.alg = alg

    def predict(self, x_train, y_train, x_pred):
        pass  # todo

    def get_clf_prob(self, x_pred):
        pass  # todo


class PredictExplore:
    def __init__(self, db, years, year, weekend):
        self.weekend = weekend

        years = sorted(set(list(years) + [year]))
        self.weekend_stats = WeekendStats(db, years, weekend)

        year_explorer = ByYearExplorer(db, year)
        weekends = year_explorer.get_names()  # weekends of this year
        self.stats = WeekendsStats(db, years, weekends)

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
        x_train = x_train.drop([WeekendExplorer.YEAR_KEY], axis=1)
        y_train = y_train.drop([WeekendExplorer.YEAR_KEY], axis=1)
        x_predict = x_predict.drop([WeekendExplorer.YEAR_KEY], axis=1)

        # drop NaN
        x_train = x_train.dropna(axis=1)  # remove weekends not in all years
        y_train = y_train.dropna(axis=1)
        x_predict = x_predict.dropna(axis=1)

        # only common weekends between X train and X pred (past years and this)
        [x_train, x_predict] = just_common_columns([x_train, x_predict])

        log_matrix("X train", x_train)
        log_matrix("Y train", y_train)
        log_matrix("X predict", x_predict)

        return x_train, y_train, x_predict

    @staticmethod
    def _post_process(data):
        pass  # todo

    def _get_clf(self):
        clf = SVC(kernel='linear', C=10, probability=True)
        return clf

    def _get_clf_prob(self, clf, x_pred):
        return clf.predict_proba(x_pred)

    def get_clf_prediction(self, x_train, y_train, x_pred):
        pass  # todo

    def _get_regr(self):
        regr = RandomForestRegressor(max_depth=5, n_estimators=100)
        return regr

    def _get_regr_data(self, regr):
        pass  # todo

    def get_prediction(self, alg, x_train, y_train, x_pred):
        alg.fit(x_train, y_train)
        return alg, alg.predict(x_pred)


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
        data = self.stats.get_race_finishes()
        x_train, y_train, x_predict = self._pre_process(data, n_years=3)
        regr = self._get_regr()
        regr, pred = self.get_prediction(regr, x_train, y_train, x_predict)
        return pred[0]  # just 1 sample -> so first value

    def get_prob_drivers_finishes(self):
        data = self.stats.get_race_finishes()
        x_train, y_train, x_predict = self._pre_process(data, n_years=3)
        clf = self._get_clf()
        clf, pred = self.get_prediction(clf, x_train, y_train, x_predict)
        prob = self._get_clf_prob(clf, x_predict)

        return pred[0], prob  # just 1 sample -> so first value

    def get_q_position_of_winner(self):
        pass  # todo

    def get_race_win_margin(self):
        data = self.stats.get_race_win_margin()
        x_train, y_train, x_predict = self._pre_process(data, n_years=3)
        regr = self._get_regr()
        regr, pred = self.get_prediction(regr, x_train, y_train, x_predict)
        return pred[0]  # just 1 sample -> so first value

    def get_q_win_margin(self):
        data = self.stats.get_q_win_margin()
        x_train, y_train, x_predict = self._pre_process(data, n_years=3)
        regr = self._get_regr()
        regr, pred = self.get_prediction(regr, x_train, y_train, x_predict)
        return pred[0]  # just 1 sample -> so first value

    def get_grand_chelem(self):
        pass  # todo
        #  will there be ? | true false -> 0, 1 -> clf (and also show prob)
