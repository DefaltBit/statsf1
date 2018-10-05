#!/usr/bin/env python3
# coding: utf-8

""" Stats models """

import numpy as np
import pandas as pd

from statsf1.explore.models import WeekendExplorer, Explorer, SummaryExplorer
from statsf1.tools.utils import get_time


class StatsExplorer(Explorer):
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


class WeekendStats(StatsExplorer):
    GRAND_CHELEM_COLUMNS = [
        "year",
        "race winner name",
        "race winner q pos",
        "race winner best lap pos",
        "q winner name",
        "q winner race pos",
        "q winner best lap pos",
        "best lap winner name",
        "best lap winner race pos",
        "best lap winner q pos",
        "grand chelem points",
        "grand chelem?"
    ]

    def __init__(self, db, years, weekend):
        super().__init__(db)

        self.years = list(years)
        self.weekend_name = self._get_weekend_collection(weekend)

    def get_grand_chelem(self):
        """
        :return: pd.DataFrame
            Race winner, q winner and best lap winner positions data. With a
            focus on the gram chelem
        """

        data = []

        for year in self.years:
            weekend = WeekendExplorer(self.db_name, year, self.weekend_name)

            # stats about race winner
            race_winner_name = weekend.get_position_summary(
                WeekendExplorer.DRIVERS_KEY,
                0
            )  # name of race winner
            race_winner_q_pos = weekend.get_driver_summary(
                WeekendExplorer.Q_POS_KEY,
                race_winner_name
            )  # q position of winner
            race_winner_best_lap_pos = weekend.get_driver_summary(
                WeekendExplorer.BEST_LAPS_POS_KEY,
                race_winner_name
            )  # best lap position of winner

            q_winner_name = weekend.get_category_key(
                "qualifications",
                "Pilote "
            )[0]  # name of q winner
            q_winner_race_pos = weekend.get_driver_summary(
                WeekendExplorer.RACE_POS_KEY,
                q_winner_name
            )  # race position of q winner
            q_winner_best_lap_pos = weekend.get_driver_summary(
                WeekendExplorer.BEST_LAPS_POS_KEY,
                q_winner_name
            )  # best lap position of q winner

            best_lap_winner_name = weekend.get_category_key(
                "best_laps",
                "Pilote "
            )[0]  # name of best lap winner
            best_lap_winner_race_pos = weekend.get_driver_summary(
                WeekendExplorer.RACE_POS_KEY,
                best_lap_winner_name
            )  # race position of best lap winner
            best_lap_winner_q_pos = weekend.get_driver_summary(
                WeekendExplorer.Q_POS_KEY,
                best_lap_winner_name
            )  # q position of best lap winner

            grand_chelem_points = np.nanmean([
                float(1) +  # position of race winner
                float(race_winner_q_pos) +
                float(race_winner_best_lap_pos)
            ])  # average positions
            grand_chelem = grand_chelem_points == 3.0

            summary = [
                year,
                race_winner_name,
                race_winner_q_pos,
                race_winner_best_lap_pos,
                q_winner_name,
                q_winner_race_pos,
                q_winner_best_lap_pos,
                best_lap_winner_name,
                best_lap_winner_race_pos,
                best_lap_winner_q_pos,
                grand_chelem_points,
                grand_chelem
            ]
            data.append(summary)

        return pd.DataFrame(data=data, columns=self.GRAND_CHELEM_COLUMNS)

        # todo race finishes per year

        # todo win margin, q maring, best lap margin


class WeekendsStats(StatsExplorer):
    def __init__(self, db, years, weekends):
        super().__init__(db)
        self.explorer = SummaryExplorer(db, years, weekends)

    def _get_summary_values(self, key, func, *args, **kwargs):
        summary = self.explorer.get_column_summary(key)

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
