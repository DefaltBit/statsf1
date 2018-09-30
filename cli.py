#!/usr/bin/env python3
# coding: utf-8


""" Command line tool """

import argparse
from enum import Enum


class AppMode(Enum):
    DOWNLOAD = "download"
    UPDATE = "update"

    @staticmethod
    def available():
        return [
            AppMode.DOWNLOAD,
            AppMode.UPDATE
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


def download():
    pass  # todo


def update():
    pass  # todo


def main():
    mode = parse_args(create_args())
    if mode == AppMode.DOWNLOAD:
        download()
    elif mode == AppMode.UPDATE:
        update()


if __name__ == '__main__':
    main()
