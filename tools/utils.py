#!/usr/bin/env python3
# coding: utf-8


""" Tools and data """

NUM_FORMAT = "{:.3f}"
MINUTES_TOKEN = "'"
SECONDS_TOKEN = "''"
PRETTY_SECONDS_TOKEN = "\""
DNF = "-"


def parse_time(time, minutes_split=MINUTES_TOKEN,
               seconds_split=PRETTY_SECONDS_TOKEN):
    minutes = float(time.split(minutes_split)[0])
    seconds = float(time.split(seconds_split)[0].split(minutes_split)[1])
    decimals = float(time.split(seconds_split)[1])
    return minutes * 60.0 + seconds + decimals / 1000.0  # seconds


def pretty_time(time):
    return time.replace(SECONDS_TOKEN, PRETTY_SECONDS_TOKEN)
