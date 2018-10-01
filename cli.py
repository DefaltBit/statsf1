#!/usr/bin/env python3
# coding: utf-8


""" Command line tool """

import argparse
import datetime
from enum import Enum

from statsf1.download import download
from statsf1.update import download as update

DATABASE_NAME = "statsf1"  # name of mongodb database to use


class AppMode(Enum):
    DOWNLOAD = "download"
    UPDATE = "update"

    @staticmethod
    def available():
        return [
            AppMode.DOWNLOAD.value,
            AppMode.UPDATE.value
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

    if mode == AppMode.DOWNLOAD.value:
        download(DATABASE_NAME)
    elif mode == AppMode.UPDATE.value:
        now = datetime.datetime.now()
        update(str(now.year), DATABASE_NAME)


if __name__ == '__main__':
    main()
