#!/usr/bin/env python3
# coding: utf-8


""" Explore database """

import abc

import numpy as np
import pandas as pd
from hal.maths.utils import get_percentage_relative_to
from hal.mongodb.models import DbBrowser

from statsf1.data import SOL
from statsf1.tools.utils import pretty_time, parse_time

# formatting
TOTAL_ENTRIES_FORMAT = SOL + "{} races\n" + \
                       SOL + "{:.2f} drivers per weekend\n" + \
                       SOL + "{:.0f} total entries"
AVAILABLE_RACES = "Available races in {}:"

# errors
NOT_FOUND_EXCEPTION = "Cannot find {} in db"
WRONG_KEY_EXCEPTION = "{} not a valid key in db. Available are {}"


def has_completed_race(laps, race_laps, ratio=0.9):
    laps = float(laps)
    race_laps = float(race_laps)
    min_laps_to_have_completed = race_laps * ratio

    return laps >= min_laps_to_have_completed


def get_position(raw_position):
    try:
        return float(raw_position)
    except:
        return np.nan  # default position when driver DNF


def get_lap(lap):
    try:
        return int(lap)
    except:
        return np.nan


def get_time(raw_time):
    try:
        raw_time = pretty_time(raw_time)
        return parse_time(raw_time)
    except:
        return np.nan


class DbNotFoundException(Exception):
    def __init__(self, to_be_found):
        super().__init__(NOT_FOUND_EXCEPTION.format(to_be_found))


class DbWrongKeyException(Exception):
    def __init__(self, key, available):
        super().__init__(WRONG_KEY_EXCEPTION.format(key, str(available)))


class Explorer:
    WEEKEND_CATEGORIES = ["race_entrants", "qualifications", "result",
                          "best_laps"]
    WEEKEND_KEYS = ["year", "name", "url"]
    WEEKEND_LABELS = WEEKEND_CATEGORIES + WEEKEND_KEYS

    def __init__(self, db):
        self.db_name = db
        self.db = DbBrowser(self.db_name)  # db browser

    def get_weekend(self, year, race):
        return [
            x
            for x in self.db.get_collection(year).find({"name": race})
        ][0]  # get first weekend found

    def count_weekends(self):
        return self.db.get_documents_count()

    @staticmethod
    def _get_year_collection(year):
        return str(year)

    @staticmethod
    def _get_weekend_collection(race_name):
        return str(race_name)

    @staticmethod
    def _is_valid_weekend(weekend):
        for key, val in weekend.items():
            if pd.isna(val):
                return False

        return True


class WeekendsExplorer(Explorer):
    def __init__(self, db):
        super().__init__(db)

        self.weekends = self._get_weekends()

    @abc.abstractmethod
    def _get_weekends(self):
        return pd.DataFrame()

    def _get_label(self, label):
        if label not in self.WEEKEND_LABELS:
            raise DbWrongKeyException(label, self.WEEKEND_LABELS)
        count = self.weekends.shape[0]  # how many weekends

        return [
            self.weekends.iloc[i][label]
            for i in range(count)
        ]

    def _get_key(self, key):
        if key not in self.WEEKEND_KEYS:
            raise DbWrongKeyException(key, self.WEEKEND_KEYS)

        labels = self._get_label(key)
        return [
            str(label)
            for label in labels
        ]

    def _get_category(self, category):
        if category not in self.WEEKEND_CATEGORIES:
            raise DbWrongKeyException(category, self.WEEKEND_CATEGORIES)

        categories = self._get_label(category)
        return [
            pd.DataFrame(data) if not pd.isna(data) else pd.DataFrame()
            for data in categories
        ]

    def get_results(self):
        return self._get_category("result")

    def get_race_entrants(self):
        return self._get_category("race_entrants")

    def get_qualifications(self):
        return self._get_category("qualifications")

    def get_best_laps(self):
        return self._get_category("best_laps")

    def get_names(self):
        return self._get_key("name")

    def get_years(self):
        return self._get_key("year")

    def get_urls(self):
        return self._get_key("url")


class ByYearExplorer(WeekendsExplorer):
    def __init__(self, db, year):
        self.year = self._get_year_collection(year)

        super().__init__(db)

    def _get_weekends(self):
        collection = self.db.get_documents_in_collection(self.year)
        return pd.DataFrame(data=collection)


class ByWeekendsExplorer(WeekendsExplorer):
    def __init__(self, db, weekend):
        self.weekend = self._get_weekend_collection(weekend)

        super().__init__(db)

    def _get_weekends(self):
        years = self.db.get_collection_names()

        return pd.DataFrame([
            [
                x
                for x in
                self.db.get_collection(year).find({"name": self.weekend})
            ][0]  # get first weekend found
            for year in years
        ])


class WeekendExplorer(Explorer):
    RACE_POS_KEY = "Race pos"
    DRIVERS_KEY = "Drivers"
    CHASSIS_KEY = "Chassis"
    Q_POS_KEY = "Q pos"
    BEST_LAPS_POS_KEY = "Best lap pos"
    RACE_FINISHES_KEY = "Race completed?"
    RACE_VS_Q_POS_KEY = "Race pos VS Q pos"
    BEST_LAP_VS_Q_TIME_KEY = "Best lap VS Q time"
    BEST_LAP_VS_Q_POS_KEY = "Best lap VS Q pos"
    EXTRA_KEYS = [RACE_FINISHES_KEY, RACE_VS_Q_POS_KEY,
                  BEST_LAP_VS_Q_TIME_KEY, BEST_LAP_VS_Q_POS_KEY]
    WEEKEND_SUMMARY_KEYS = [RACE_POS_KEY, DRIVERS_KEY, CHASSIS_KEY,
                            RACE_FINISHES_KEY, Q_POS_KEY, RACE_VS_Q_POS_KEY,
                            BEST_LAPS_POS_KEY, BEST_LAP_VS_Q_POS_KEY,
                            BEST_LAP_VS_Q_TIME_KEY]

    def __init__(self, db, year, weekend):
        super().__init__(db)

        self.year = self._get_year_collection(year)
        self.weekend_name = self._get_weekend_collection(weekend)
        self.weekend = self.get_weekend(self.year, self.weekend_name)

    def _get_label(self, label):
        if label not in self.WEEKEND_LABELS:
            raise DbWrongKeyException(label, self.WEEKEND_LABELS)

        try:
            return self.weekend[label]
        except:
            return {}

    def _get_key(self, key):
        if key not in self.WEEKEND_KEYS:
            raise DbWrongKeyException(key, self.WEEKEND_KEYS)

        label = self._get_label(key)
        return str(label)

    def _get_category(self, category):
        if category not in self.WEEKEND_CATEGORIES:
            raise DbWrongKeyException(category, self.WEEKEND_CATEGORIES)

        data = self._get_label(category)
        if not pd.isna(data):
            return pd.DataFrame(data)

        return pd.DataFrame()

    def get_category_key(self, category, key, driver_order=None):
        category_data = self._get_category(category)
        available_keys = list(category_data.keys())
        if key not in available_keys:
            raise DbWrongKeyException(key, available_keys)

        data = category_data[key]

        if driver_order is not None:
            original_drivers = pd.DataFrame(category_data["Pilote "])
            ordered_data = []
            for driver in driver_order:
                try:
                    index = original_drivers["Pilote "] == driver
                    index = original_drivers.index[index].tolist()[0]  # first
                    ordered_data.append(data[index])
                except:
                    ordered_data.append(np.nan)

            data = ordered_data

        return data

    def get_results(self):
        return self._get_category("result")

    def get_race_entrants(self):
        return self._get_category("race_entrants")

    def get_qualifications(self):
        return self._get_category("qualifications")

    def get_best_laps(self):
        return self._get_category("best_laps")

    def get_name(self):
        return self._get_key("name")

    def get_year(self):
        return self._get_key("year")

    def get_url(self):
        return self._get_key("url")

    def get_race_finishes(self, drivers):
        laps = self.get_category_key("result", "Tour ", driver_order=drivers)
        laps = [
            get_lap(lap)
            for lap in laps
        ]
        race_laps = max(laps)
        laps = pd.Series(laps)
        laps.apply(has_completed_race, race_laps=race_laps)

        return pd.DataFrame(laps, columns=[self.RACE_FINISHES_KEY])

    def get_race_vs_q_pos(self, drivers):
        race_pos = self.get_category_key(
            "result", "Pos ", driver_order=drivers
        )
        q_pos = self.get_category_key(
            "qualifications", "Pos ", driver_order=drivers
        )

        race_vs_q = [
            get_position(race) - get_position(q)
            for (race, q) in zip(race_pos, q_pos)
        ]

        return pd.DataFrame(race_vs_q, columns=[self.RACE_VS_Q_POS_KEY])

    def get_best_lap_vs_q_pos(self, drivers):
        best_laps_pos = self.get_category_key(
            "best_laps", "n ", driver_order=drivers
        )
        q_pos = self.get_category_key(
            "qualifications", "Pos ", driver_order=drivers
        )

        best_lap_vs_q = [
            get_position(lap) - get_position(q)
            for (lap, q) in zip(best_laps_pos, q_pos)
        ]

        return pd.DataFrame(best_lap_vs_q, columns=[self.BEST_LAP_VS_Q_POS_KEY])

    def get_best_lap_vs_q_time(self, drivers):
        best_lap_times = self.get_category_key(
            "best_laps", "Temps ", driver_order=drivers
        )
        q_times = self.get_category_key(
            "qualifications", "Temps ", driver_order=drivers
        )

        best_lap_vs_q = [
            get_percentage_relative_to(
                get_time(best_lap_time),
                get_time(q_time)
            )
            for (best_lap_time, q_time) in
            zip(best_lap_times, q_times)
        ]  # order by best lap times

        return pd.DataFrame(best_lap_vs_q,
                            columns=[self.BEST_LAP_VS_Q_TIME_KEY])

    def get_summary(self):
        # todo add more labels
        race_pos = pd.DataFrame(
            self.get_category_key("result", "Pos ").tolist(),
            columns=[self.RACE_POS_KEY]
        )
        driver_order = self.get_category_key("result", "Pilote ").tolist()
        drivers = pd.DataFrame(
            driver_order,
            columns=[self.DRIVERS_KEY]
        )

        chassis = pd.DataFrame(
            self.get_category_key("result", "Ch\\xc3\\xa2ssis ").tolist(),
            columns=[self.CHASSIS_KEY]
        )
        race_finishes = self.get_race_finishes(driver_order)
        q_pos = pd.DataFrame(
            self.get_category_key(
                "qualifications", "Pos ", driver_order=driver_order
            ),
            columns=[self.Q_POS_KEY]
        )
        race_vs_q_pos = self.get_race_vs_q_pos(driver_order)
        best_lap_pos = pd.DataFrame(
            self.get_category_key(
                "best_laps", "n ", driver_order=driver_order
            ),
            columns=[self.BEST_LAPS_POS_KEY]
        )
        best_lap_vs_q_pos = self.get_best_lap_vs_q_pos(driver_order)
        best_lap_vs_q_time = self.get_best_lap_vs_q_time(driver_order)

        summary = race_pos.join(drivers).join(chassis).join(race_finishes) \
            .join(q_pos).join(race_vs_q_pos).join(best_lap_pos) \
            .join(best_lap_vs_q_pos).join(best_lap_vs_q_time)  # concatenate
        return summary

    def get_driver_summary(self, key, driver):
        summary = self.get_summary()
        row = summary.loc[summary[self.DRIVERS_KEY] == driver]
        return row[key].tolist()[0]

    def get_chassis_summary(self, key, driver):
        summary = self.get_summary()
        row = summary.loc[summary[self.CHASSIS_KEY] == driver]
        return row[key].tolist()[0]  # todo average of the positions

    def get_position_summary(self, key, position):
        summary = self.get_summary()
        row = summary.loc[position]
        return row[key]


class SummaryExplorer(Explorer):
    def __init__(self, db, years):
        super().__init__(db)

        self.years = list(years)
        self.weekends = self._get_weekends()

    def _get_weekends(self):
        weekends_list = []

        for year in self.years:
            weekends_names = ByYearExplorer(self.db_name, year).get_names()
            weekends = [
                WeekendExplorer(self.db_name, year, weekend)
                for weekend in weekends_names
            ]
            df = pd.DataFrame(
                data=[weekends],
                columns=weekends_names
            )

            weekends_list.append(df)

        return weekends_list

    def _get_yearly_summary(self, summary):
        for year, (i, year_summary) in zip(self.years, enumerate(summary)):
            summary[i].insert(0, "Year", [year])

        summary = pd.concat(summary, sort=False)
        return summary

    def get_driver_summary(self, key, driver):
        summary = []

        for year_weekends in self.weekends:
            data = []
            for weekend_name in year_weekends.keys():
                weekend = year_weekends[weekend_name][0]
                try:
                    data.append(weekend.get_driver_summary(key, driver))
                except:
                    data.append(np.nan)

            df = pd.DataFrame(
                data=[data],
                columns=year_weekends.columns
            )
            summary.append(df)

        return self._get_yearly_summary(summary)

    def get_chassis_summary(self, key, chassis):
        summary = []

        for year_weekends in self.weekends:
            data = []
            for weekend_name in year_weekends.keys():
                weekend = year_weekends[weekend_name][0]
                try:
                    data.append(weekend.get_chassis_summary(key, chassis))
                except:
                    data.append(np.nan)

            df = pd.DataFrame(
                data=[data],
                columns=year_weekends.columns
            )
            summary.append(df)

        return self._get_yearly_summary(summary)

    def get_position_summary(self, key, position):
        summary = []

        for year_weekends in self.weekends:
            data = []
            for weekend_name in year_weekends.keys():
                weekend = year_weekends[weekend_name][0]
                try:
                    data.append(weekend.get_position_summary(key, position))
                except:
                    data.append(np.nan)

            df = pd.DataFrame(
                data=[data],
                columns=year_weekends.columns
            )
            summary.append(df)

        return self._get_yearly_summary(summary)
