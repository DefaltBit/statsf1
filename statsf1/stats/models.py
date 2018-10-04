#!/usr/bin/env python3
# coding: utf-8


""" Gets stats about db """

import numpy as np
import pandas as pd
from hal.streams.pretty_table import pretty_df

from statsf1.data import NUM_FORMAT, NORM_PROB_FORMAT, SOL, LOW_NUM_FORMAT
from statsf1.explore.models import SummaryExplorer, WeekendExplorer
from statsf1.tools.utils import get_time

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
    def __init__(self, db, years, races):
        super().__init__(db, years, races)

    @staticmethod
    def _parse_values(values, nan_value):
        return [
            value if not pd.isna(value) else nan_value
            for value in values
        ]

    @staticmethod
    def _count_race_finishes(values):
        return values.count(True)

    @staticmethod
    def _get_win_margin(times):
        first_time = get_time(times[0])
        second_time = get_time(times[1])
        time_delta = float(first_time - second_time)

        return time_delta

    @staticmethod
    def _get_winner(values):
        return values[0]

    def _get_summary_values(self, key, func, *args, **kwargs):
        summary = self.get_column_summary(key)

        for row in range(summary.shape[0]):
            for col in range(1, summary.shape[1]):  # not count year
                weekend_column = summary.iloc[row][col]

                try:
                    weekend_column = self._parse_values(weekend_column, False)
                    summary.iloc[row, col] = func(weekend_column, *args,
                                                  **kwargs)
                except:
                    summary.iloc[row, col] = np.nan

        return summary

    def get_race_finishes(self):
        return self._get_summary_values(
            WeekendExplorer.RACE_FINISHES_KEY,
            self._count_race_finishes
        )

    def get_q_win_margin(self):
        return self._get_summary_values(
            WeekendExplorer.Q_TIME_KEY,
            self._get_win_margin
        )

    def get_race_win_margin(self):
        return self._get_summary_values(
            WeekendExplorer.RACE_TIME_KEY,
            self._get_win_margin
        )

    def get_race_winner_q_position(self):
        return self._get_summary_values(
            WeekendExplorer.Q_POS_KEY,
            self._get_winner
        )


def main():
    db = "statsf1"
    max_year = 2017
    min_year = 2015
    years = range(min_year, max_year + 1)
    races = ["Japon", "Italie", "Australie"]

    e = Statistician(db, years, races)
    s = e.get_race_finishes()
    print(pretty_df(s))

    e = WeekendExplorer(db, 2015, "Australie")
    s = e.get_summary()
    print(pretty_df(s))


if __name__ == '__main__':
    main()
