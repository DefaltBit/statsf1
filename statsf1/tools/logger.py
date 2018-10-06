#!/usr/bin/env python3
# coding: utf-8


""" App tools """

import logging
import threading

# formatting
from hal.streams.pretty_table import pretty_df

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

# messages
MATRIX_FORMAT = "{}: {} rows x {} columns"


def get_logger():
    return LOGGER


def log_matrix(name, matrix, show_values=False):
    logger = get_logger()

    rows = matrix.shape[0]
    columns = matrix.shape[1]
    message = MATRIX_FORMAT.format(name, rows, columns)

    logger.debug(message)

    if show_values:
        print(pretty_df(matrix))


def log_ml_algorithm(algorithm):
    pass  # todo


def log_error(race, cause=None):
    logger = get_logger()
    thread_id = threading.current_thread().ident
    text = race.text + " " + race.year
    if cause:
        text += " due to " + str(cause)

    logger.error(LOG_THREAD_FORMAT.format(thread_id, text, race.url))
