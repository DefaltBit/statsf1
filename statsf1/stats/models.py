#!/usr/bin/env python3
# coding: utf-8

""" Stats models """

import numpy as np
import pandas as pd

from statsf1.explore.models import WeekendExplorer, Explorer


class WeekendStats(Explorer):
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

    def __init__(self, db, weekend, years):
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
