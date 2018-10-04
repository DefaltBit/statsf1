#!/usr/bin/env python3
# coding: utf-8


""" Tools and data """

import numpy as np

from statsf1.tools.parse import pretty_time, parse_time


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
