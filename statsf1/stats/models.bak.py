#!/usr/bin/env python3
# coding: utf-8


""" Gets stats about db """

import numpy as np
import pandas as pd

from statsf1.explore.models import SummaryExplorer, WeekendExplorer
from statsf1.tools.utils import get_time


class Statistician(SummaryExplorer):
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
