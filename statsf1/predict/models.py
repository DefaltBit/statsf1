#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from hal.data.matrix import Matrix
from hal.streams.pretty_table import pretty_format_table
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingClassifier

from statsf1.data import SOL, NUM_FORMAT, TOL
from statsf1.stats.models import Statistician

# format
PREDICT_FORMAT = SOL + "Prediction at {} in {} using last {} " \
                       "years\n    {}"
MATRIX_SHAPE_FORMAT = "Shape of matrix is {} rows x {} columns"
STANDINGS_FORMAT = "{:2.0f}) {}"

# messages
COEFFS_MESSAGE = SOL + "Coefficient of each class"


class Predictor:
    def __init__(self, race, year, db, n_years):
        self.stats = Statistician(race, year, db, n_years)
        self.explorer = self.stats.explorer

        self.years_before = 3
        self.max_iterations = 10000

        self.regr = AdaBoostRegressor()
        self.clf = GradientBoostingClassifier()

        self.rows = None
        self.columns = None
        self.matrix = None
        self.lb = None

    def _get_data(self, data_label, driver=None, chassis=None, years_before=3):
        self.rows, self.columns, matrix = self.stats.get_matrix(
            data_label, driver=driver, chassis=chassis
        )

        previous_data = Statistician(
            self.explorer.raw_race,
            str(int(self.explorer.raw_year) - 1),
            self.explorer.db_name,
            self.stats.n_years + years_before
        ).get_race_matrix(data_label, driver=driver, chassis=chassis)[1]

        for year in range(1, years_before + 1):  # update labels
            self.columns.append(self.explorer.raw_race + "-" + str(year))

        for i, row in enumerate(matrix):
            for year in range(years_before):
                matrix[i].append(previous_data[i + year])

        self._preprocess(matrix)

    def _preprocess(self, matrix):
        matrix = Matrix(matrix)  # prep-process: encode matrix
        self.matrix = matrix

        # todo self.lb, self.matrix = matrix.encode()

    def _get_train_pred(self):
        _, x = self.matrix.remove_column(
            self.columns, self.explorer.raw_race
        )
        y = self.matrix.get_column(
            self.columns.index(self.explorer.raw_race)
        )

        num_features = len(x[0])
        x_train = [row for row in x[1:]]  # do NOT train on this year data
        y_train = [val for val in y[1:]]
        x_pred = x[0].reshape(1, num_features)  # vector to make predictions on

        return x_train, y_train, x_pred

    def _postprocess_regr(self, pred_num):
        pred = pred_num[0]
        coeffs = None  # todo self.regr.estimator_errors_  # coefficients
        classes = [
            race
            for race in self.columns
            if race != self.explorer.raw_race
        ]

        return pred, coeffs, classes

    def _postprocess_clf(self, pred_num):
        pred = pred_num[0]  # todo self.lb.inverse_transform(pred_num)[0]
        coeffs = None  # todo self.clf.predict_proba(x_pred)[0]

        classes = [
            race
            for race in self.columns
            if race != self.explorer.raw_race
        ]

        return pred, coeffs, classes

    def _predict_clf(self):
        x_train, y_train, x_pred = self._get_train_pred()  # split

        self.clf.fit(x_train, y_train)  # fit
        pred_num = self.clf.predict(x_pred)  # predict

        pred, coeffs, classes = self._postprocess_clf(pred_num)  # post-process

        return pred, coeffs, classes

    def _predict_regr(self):
        for i, row in enumerate(self.matrix.matrix):
            for j, col in enumerate(row):
                self.matrix.matrix[i][j] = float(self.matrix.matrix[i][j])

        x_train, y_train, x_pred = self._get_train_pred()  # split

        self.regr.fit(x_train, y_train)  # fit
        pred_num = self.regr.predict(x_pred)  # predict

        pred, coeffs, classes = self._postprocess_regr(pred_num)  # post

        return pred, coeffs, classes

    def _get_q_driver_pos(self, driver):
        self._get_data("Q pos", driver=driver,
                       years_before=self.years_before)
        return self._predict_clf()

    def _get_q_chassis_pos(self, chassis):
        self._get_data("Q pos", chassis=chassis,
                       years_before=self.years_before)
        return self._predict_clf()

    def _get_race_driver_pos(self, driver):
        self._get_data("race pos", driver=driver,
                       years_before=self.years_before)
        return self._predict_clf()

    def print_race_driver_pos(self):
        pass  # todo

    def _get_race_chassis_pos(self, chassis):
        self._get_data("race pos", chassis=chassis,
                       years_before=self.years_before)
        return self._predict_clf()

    def print_race_chassis_pos(self, chassis, with_coeffs=True):
        pred, coeffs, classes = self._get_race_chassis_pos(chassis)

        print(PREDICT_FORMAT.format(
            self.explorer.raw_race, self.explorer.raw_year,
            self.stats.n_years, pred
        ))

        if with_coeffs:
            print(COEFFS_MESSAGE)
            coeffs = [
                NUM_FORMAT.format(coeff)
                for coeff in coeffs
            ]
            print(pretty_format_table(classes, [coeffs]))

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


def print_standings(data):
    for chassis, position in sorted(data.items(), key=lambda x: x[0]):
        print(STANDINGS_FORMAT.format(float(position), chassis))


def run(race, year, n_years, db):
    available_drivers = Statistician(race, year, db, n_years).get_drivers()
    available_chassis = Statistician(race, year, db, n_years).get_chassis()
    predictor = Predictor(race, year, db, n_years)

    print(TOL + "Qualifications standings")
    data = {
        driver: predictor._get_q_driver_pos(driver)[0]
        for driver in available_drivers
    }
    print(SOL + "drivers")
    print_standings(data)

    data = {
        chassis: predictor._get_race_chassis_pos(chassis)[0]
        for chassis in available_chassis
    }
    print(SOL + "chassis")
    print_standings(data)

    print(TOL + "Race standings")
    data = {
        driver: predictor._get_race_driver_pos(driver)[0]
        for driver in available_drivers
    }
    print(SOL + "drivers")
    print_standings(data)

    data = {
        chassis: predictor._get_race_chassis_pos(chassis)[0]
        for chassis in available_chassis
    }
    print(SOL + "chassis")
    print_standings(data)
