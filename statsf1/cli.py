#!/usr/bin/env python3
# coding: utf-8


""" Command line tool """

import argparse
from enum import Enum

from statsf1.explore import run as explore
from statsf1.predict.models import run as predict
from statsf1.stats.models import run as stats

DATABASE_NAME = "statsf1"  # name of mongodb database to use


class AppMode(Enum):
    EXPLORE = "explore"
    STATS = "stats"
    PREDICT = "predict"

    @staticmethod
    def available():
        return [
            AppMode.EXPLORE.value,
            AppMode.STATS.value,
            AppMode.PREDICT.value
        ]


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(
        usage="-m <operations mode>"
    )

    parser.add_argument(
        "-m",
        dest="mode",
        help="mode to run app; must be in " + str(AppMode.available()),
        required=True
    )

    return parser


def parse_args(parser):
    """
    :param parser: ArgumentParser
        Object that holds cmd arguments.
    :return: tuple
        Values of arguments.
    """

    args = parser.parse_args()

    mode = str(args.mode)
    if mode in AppMode.available():
        return mode

    return None


def main():
    mode = parse_args(create_args())

    race = "Japon"
    driver = "Lewis HAMILTON"
    n_years = 5

    if mode == AppMode.EXPLORE.value:
        explore(DATABASE_NAME)
    elif mode == AppMode.STATS.value:
        year = 2017
        n_drivers = 20
        stats(race, driver, year, n_years, n_drivers, DATABASE_NAME)
    elif mode == AppMode.PREDICT.value:
        year = 2018
        predict(race, year, n_years, DATABASE_NAME)


if __name__ == '__main__':
    main()
