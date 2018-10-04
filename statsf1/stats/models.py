#!/usr/bin/env python3
# coding: utf-8


""" Gets stats about db """

import numpy as np
import pandas as pd
from scipy.stats import norm

from statsf1.data import NUM_FORMAT, NORM_PROB_FORMAT, SOL, LOW_NUM_FORMAT, \
    TOL
from statsf1.explore.models import SummaryExplorer, WeekendExplorer
from statsf1.tools.parse import parse_time

# formatting
COMPLETES_FORMAT = "# past years = {}\n" \
                   "ratio of completes = " + NORM_PROB_FORMAT + "\n" \
                                                                "# drivers = {} =>\n" \
                                                                "# completes = " + NUM_FORMAT + " +- " + NUM_FORMAT
PROB_FORMAT = "P({}) = " + NUM_FORMAT
NORM_DISTRIBUTION_FORMAT = SOL + "normal distribution " + NORM_PROB_FORMAT
RACE_SUMMARY_FORMAT = SOL + "summary of {} in {}"
DRIVER_SUMMARY_FORMAT = SOL + "summary of {} at {} from {} to {}"
COMPLETES_MESSAGE = SOL + "who complets? Everyone, except the following:"

# probability messages
PROB_VS_STAKE_MESSAGE = SOL + "probability VS stakes (more is better)"
LT_PROB_FORMAT = "P(< " + LOW_NUM_FORMAT + ") = " + NUM_FORMAT
IN_BETWEEN_PROB_FORMAT = "P(" + LOW_NUM_FORMAT + " < " + LOW_NUM_FORMAT + \
                         ") = " + NUM_FORMAT
GT_PROB_FORMAT = "P(> " + LOW_NUM_FORMAT + ") = " + NUM_FORMAT


def print_probabilities(stakes, probabilities, messages):
    most_probable = max(probabilities)
    lists = zip(stakes, probabilities, messages)
    for i, (stake, prob, message) in enumerate(lists):
        try:
            msg = message.format(stake, prob)
        except:
            msg = message.format(stakes[i - 1], stake, prob)

        msg = "{:>21}".format(msg)

        if prob == most_probable:
            msg += " <-- best"

        print(msg)


def print_probabilities_summary(title, labels, probabilities, stakes, messages):
    print(title)
    print_probabilities(
        labels,
        probabilities,
        messages
    )

    print(PROB_VS_STAKE_MESSAGE)
    print_probabilities(
        labels,
        stakes,
        messages
    )


def get_probabilities(stakes):
    return [
        1.0 / stake
        for stake in stakes
    ]  # calculate probability of each stake


def compare_to_stakes(probabilities, stakes):
    return [
        prob / stake * prob
        for prob, stake in zip(probabilities, stakes)
    ]  # compare predicted probability with staked one


class Statistician(SummaryExplorer):
    def __init__(self, db, years):
        super().__init__(db, years)

    @staticmethod
    def _parse_values(values, nan_value):
        return [
            value if not pd.isna(value) else nan_value
            for value in values
        ]

    def get_race_finishes(self):
        summary = self.get_column_summary(WeekendExplorer.RACE_FINISHES_KEY)

        for row in range(summary.shape[0]):
            for col in range(1, summary.shape[1]):  # not count year
                weekend_column = summary.iloc[row][col]

                try:
                    weekend_column = self._parse_values(weekend_column, False)
                    race_finishes = weekend_column.count(True)
                    summary.iloc[row, col] = race_finishes
                except:
                    summary.iloc[row, col] = np.nan

        return summary


    def _get_qualify_margin(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {
            year: parse_time(data[1][7]) - parse_time(data[0][7])
            for year, data in summaries.items()
        }
        x = [
            diff for year, diff in summary.items()
        ]

        return norm.fit(x)


    def _get_race_margin(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {
            year: parse_time(data[1][5]) - parse_time(data[0][5])
            for year, data in summaries.items()
        }
        x = [
            diff for year, diff in summary.items()
        ]

        return norm.fit(x)


    def _get_winner_q_position(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {
            year: float(data[0][6])  # position of winner in qualifications
            for year, data in summaries.items()
        }
        x = [
            pos for year, pos in summary.items()
        ]

        return norm.fit(x)


def run(race, driver, year, n_years, n_drivers, db):
    stats = Statistician(race, year, db, n_years)

    print(TOL + "# drivers who complete the race")
    stats.print_race_completes(n_drivers, STAKES["completes"])

    print(TOL + "Drivers who complete the race")
    stats.print_driver_completes()

    print(TOL + "Q time win margin")
    stats.print_qualify_margin(STAKES["q_margin"])

    print(TOL + "Race time win margin")
    stats.print_race_margin(STAKES["race_margin"])

    print(TOL + "Q position of winner")
    stats.print_winner_q_position(n_drivers, STAKES["win_q_pos"])

    print(TOL + "Race summary")
    stats.print_summary()

    print(TOL + "Driver summary")
    stats.print_driver_summary(driver)
