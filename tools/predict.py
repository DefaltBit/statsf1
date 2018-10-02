#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from hal.data.matrix import Matrix
from hal.streams.pretty_table import pretty_format_table
from sklearn.linear_model import LogisticRegression

from statsf1.data import SOL, NUM_FORMAT, TOL
from statsf1.tools.stats import Statistician

# format
PREDICT_FORMAT = SOL + "Prediction at {} in {} using last {} " \
                       "years\n    {}"

# messages
COEFFS_MESSAGE = SOL + "Probabilities of classes"


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

        classes = ml.classes_.tolist()  # prediction classes
        coeffs = ml.predict_proba(x_pred)[0]  # probabilities of classes

        return pred, coeffs, lb.inverse_transform(classes)

    def print_race_chassis_win(self):
        clf = LogisticRegression(solver='lbfgs', multi_class='multinomial',
                                 max_iter=1000)
        pred, coeffs, classes = self._predict(clf, "chassis")

        print(PREDICT_FORMAT.format(
            self.explorer.raw_race, self.explorer.raw_year,
            self.stats.n_years, pred
        ))

        print(COEFFS_MESSAGE)
        coeffs = [
            NUM_FORMAT.format(coeff)
            for coeff in coeffs
        ]
        print(pretty_format_table(classes, [coeffs]))

    def print_race_driver_win(self):
        clf = LogisticRegression(solver='lbfgs', multi_class='multinomial',
                                 max_iter=1000)
        pred, coeffs, classes = self._predict(clf, "driver")

        print(PREDICT_FORMAT.format(
            self.explorer.raw_race, self.explorer.raw_year,
            self.stats.n_years, pred
        ))

        print(COEFFS_MESSAGE)
        coeffs = [
            NUM_FORMAT.format(coeff)
            for coeff in coeffs
        ]
        print(pretty_format_table(classes, [coeffs]))

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

    print(TOL + "Chassis winner")
    pred.print_race_chassis_win()

    print(TOL + "Driver winner")
    pred.print_race_driver_win()
