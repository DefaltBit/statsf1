#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from hal.data.matrix import Matrix
from sklearn.linear_model import ElasticNet

from statsf1.tools.stats import Statistician


class Predictor:
    def __init__(self, race, year, db, n_years):
        self.stats = Statistician(race, year, db, n_years)
        self.explorer = self.stats.explorer

    def _predict(self, ml, label):
        rows, columns, matrix = self.stats.get_races_matrix(label)

        matrix = Matrix(matrix)  # prep-process: encode matrix
        lb, matrix_num = matrix.encode()

        _, x = matrix_num.remove_column(columns, self.explorer.raw_race)
        y = matrix_num.get_column(columns.index(self.explorer.raw_race))

        num_features = len(x[0])
        x_train = [row for row in x[1:]]  # do NOT train on predict data
        y_train = [val for val in y[1:]]
        x_pred = x[0].reshape(1, num_features)  # vector to make predictions on

        ml.fit(x_train, y_train)  # fit
        pred_num = ml.predict(x_pred)  # predict

        pred = lb.inverse_transform(pred_num)[0]  # post-process: decode
        return pred, ml.coef_

    def print_race_chassis_win(self):
        clf, coeffs = ElasticNet()
        pred = self._predict(clf, "chassis")

        print(pred)  # todo

    def print_race_driver_win(self):
        clf, coeffs = ElasticNet()
        pred = self._predict(clf, "driver")

        print(pred)  # todo

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


def run(race, driver, year, n_years, db):
    pred = Predictor(race, year, db, n_years)
    pred.print_race_chassis_win()
