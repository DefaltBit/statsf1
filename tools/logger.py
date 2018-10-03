#!/usr/bin/env python3
# coding: utf-8


""" App tools """

import logging
import threading

# formatting
LOG_THREAD_FORMAT = "thread-{} {} {}"
LOG_RACES_FORMAT = "Found {} races"
LOG_GOT_FORMAT = "Got {}"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

LOG_LEVEL = logging.DEBUG

LOGGER = logging.getLogger("statsf1")
LOGGER.setLevel(LOG_LEVEL)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(LOG_LEVEL)
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_FORMAT))

LOGGER.addHandler(STREAM_HANDLER)


def get_logger():
    return LOGGER


def log_races(races):
    logger = get_logger()
    logger.debug(LOG_RACES_FORMAT.format(len(races)))


def log_race(race):
    logger = get_logger()
    thread_id = threading.current_thread().ident
    logger.debug(LOG_THREAD_FORMAT.format(thread_id, race.text, race.year))


def log_year(year):
    logger = get_logger()
    logger.debug(LOG_GOT_FORMAT.format(str(year)))


def log_error(race, cause=None):
    logger = get_logger()
    thread_id = threading.current_thread().ident
    text = race.text + " " + race.year
    if cause:
        text += " because " + str(cause)

    logger.error(LOG_THREAD_FORMAT.format(thread_id, text, race.url))
