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

    @staticmethod
    def _get_summary_values(summary, nan_value, func, *args, **kwargs):
        for row in range(summary.shape[0]):
            for col in range(1, summary.shape[1]):  # not count year
                weekend_column = summary.iloc[row][col]

                try:
                    weekend_column = StatsExplorer._parse_values(
                        weekend_column, nan_value  # False in case of NaN
                    )
                    summary.iloc[row, col] = func(weekend_column, *args,
                                                  **kwargs)
                except:
                    summary.iloc[row, col] = np.nan

        return summary


class WeekendStats(StatsExplorer):
    GRAND_CHELEM_KEY = "Grand chelem?"
    GRAND_CHELEM_COLUMNS = [
        WeekendExplorer.YEAR_KEY,
        "Race winner: name",
        "Race winner: " + WeekendExplorer.Q_POS_KEY.lower(),
        "Race winner: " + WeekendExplorer.BEST_LAPS_POS_KEY.lower(),
        "Q winner: name",
        "Q winner: " + WeekendExplorer.RACE_POS_KEY.lower(),
        "Q winner: " + WeekendExplorer.BEST_LAPS_POS_KEY.lower(),
        "Best lap winner: name",
        "Best lap winner: " + WeekendExplorer.RACE_POS_KEY.lower(),
        "Best lap winner: " + WeekendExplorer.Q_POS_KEY.lower(),
        GRAND_CHELEM_KEY
    ]
    RACE_FINISHES_COLUMNS = [
        WeekendExplorer.YEAR_KEY,
        WeekendExplorer.RACE_FINISHES_KEY
    ]
    RACE_Q_BEST_LAP_WIN_MARGIN_COLUMNS = [
        WeekendExplorer.YEAR_KEY,
        "Race winner: name",
        "Race win margin",
        "Q winner: name",
        "Q win margin",
        "Best lap winner: name",
        "Best lap win margin"
    ]

    def __init__(self, db, years, weekend):
        super().__init__(db)
        self.explorers = [
            WeekendExplorer(db, year, weekend)
            for year in years
        ]

    def get_grand_chelem(self):
        """
        :return: pd.DataFrame
            Race winner, q winner and best lap winner positions data. With a
            focus on the gram chelem
        """

        data = []

        for explorer in self.explorers:
            # stats about race winner
            race_winner_name = explorer.get_position_summary(
                WeekendExplorer.DRIVERS_KEY,
                0
            )  # name of race winner
            race_winner_q_pos = explorer.get_driver_summary(
                WeekendExplorer.Q_POS_KEY,
                race_winner_name
            )  # q position of winner
            race_winner_best_lap_pos = explorer.get_driver_summary(
                WeekendExplorer.BEST_LAPS_POS_KEY,
                race_winner_name
            )  # best lap position of winner

            q_winner_name = explorer.get_category_key(
                "qualifications",
                "Pilote "
            )[0]  # name of q winner
            q_winner_race_pos = explorer.get_driver_summary(
                WeekendExplorer.RACE_POS_KEY,
                q_winner_name
            )  # race position of q winner
            q_winner_best_lap_pos = explorer.get_driver_summary(
                WeekendExplorer.BEST_LAPS_POS_KEY,
                q_winner_name
            )  # best lap position of q winner

            best_lap_winner_name = explorer.get_category_key(
                "best_laps",
                "Pilote "
            )[0]  # name of best lap winner
            best_lap_winner_race_pos = explorer.get_driver_summary(
                WeekendExplorer.RACE_POS_KEY,
                best_lap_winner_name
            )  # race position of best lap winner
            best_lap_winner_q_pos = explorer.get_driver_summary(
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
                explorer.year,
                race_winner_name,
                race_winner_q_pos,
                race_winner_best_lap_pos,
                q_winner_name,
                q_winner_race_pos,
                q_winner_best_lap_pos,
                best_lap_winner_name,
                best_lap_winner_race_pos,
                best_lap_winner_q_pos,
                grand_chelem
            ]
            data.append(summary)

        return pd.DataFrame(data=data, columns=self.GRAND_CHELEM_COLUMNS)

    def get_race_finishes(self):
        data = []

        for explorer in self.explorers:
            drivers = explorer.get_category_key("result", "Pilote ").tolist()
            race_finishes = explorer.get_race_finishes(drivers)
            race_finishes = race_finishes[
                WeekendExplorer.RACE_FINISHES_KEY].tolist()
            race_finishes = self._count_race_finishes(race_finishes)

            summary = [
                explorer.year,
                race_finishes
            ]

            data.append(summary)

        return pd.DataFrame(data=data, columns=self.RACE_FINISHES_COLUMNS)

    def get_race_q_best_lap_win_margin(self):
        data = []

        for explorer in self.explorers:
            race_times = explorer.get_category_key("result", "\xa0")
            q_times = explorer.get_category_key("qualifications", "Temps ")
            best_lap_times = explorer.get_category_key("best_laps", "Temps ")

            race_win_margin = self._get_win_margin(race_times.tolist())
            q_win_margin = self._get_win_margin(q_times.tolist())
            best_lap_win_margin = self._get_win_margin(best_lap_times.tolist())

            race_winner_name = explorer.get_position_summary(
                WeekendExplorer.DRIVERS_KEY,
                0
            )  # name of race winner
            q_winner_name = explorer.get_category_key(
                "qualifications",
                "Pilote "
            )[0]  # name of q winner
            best_lap_winner_name = explorer.get_category_key(
                "best_laps",
                "Pilote "
            )[0]  # name of best lap winner

            summary = [
                explorer.year,
                race_winner_name,
                race_win_margin,
                q_winner_name,
                q_win_margin,
                best_lap_winner_name,
                best_lap_win_margin
            ]

            data.append(summary)

        return pd.DataFrame(data=data,
                            columns=self.RACE_Q_BEST_LAP_WIN_MARGIN_COLUMNS)


class WeekendsStats(StatsExplorer):
    def __init__(self, db, years, weekends):
        super().__init__(db)
        self.explorer = SummaryExplorer(db, years, weekends)

    def get_race_finishes(self):
        summary = self.explorer.get_column_summary(
            WeekendExplorer.RACE_FINISHES_KEY)
        nan_value = False
        return self._get_summary_values(summary, nan_value,
                                        self._count_race_finishes)

    def get_q_win_margin(self):
        summary = self.explorer.get_column_summary(WeekendExplorer.Q_TIME_KEY)
        nan_value = str(float("inf"))
        return self._get_summary_values(summary, nan_value,
                                        self._get_win_margin)

    def get_race_win_margin(self):
        summary = self.explorer.get_column_summary(
            WeekendExplorer.RACE_TIME_KEY)
        nan_value = str(float("inf"))
        return self._get_summary_values(summary, nan_value,
                                        self._get_win_margin)

    def get_bets_lap_win_margin(self):
        summary = self.explorer.get_column_summary(
            WeekendExplorer.BEST_LAPS_TIME_KEY)
        nan_value = str(float("inf"))
        return self._get_summary_values(summary, nan_value,
                                        self._get_win_margin)

    def get_race_winner_q_position(self):
        summary = self.explorer.get_column_summary(WeekendExplorer.Q_POS_KEY)
        nan_value = float("inf")  # DNF
        return self._get_summary_values(summary, nan_value, self._get_winner)
