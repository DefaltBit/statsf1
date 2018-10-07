#!/usr/bin/env python3
# coding: utf-8


""" App tools """

import logging
import threading

# formatting
from hal.streams.pretty_table import pretty_df

from tools.utils import get_class_name

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


def log_matrix(name, matrix, row_names=None, show_values=False):
    rows = matrix.shape[0]
    columns = matrix.shape[1]
    message = MATRIX_FORMAT.format(name, rows, columns)

    get_logger().debug(message)

    if rows:
        get_logger().debug("Rows: " + str(row_names))

    if show_values:
        pretty_matrix = pretty_df(matrix)
        for line in pretty_matrix.split("\n"):
            get_logger().debug(line)


def log_ml_algorithm(algorithm):
    name = get_class_name(algorithm)
    get_logger().debug(name + " has been trained, ready to predict")


def log_error(race, cause=None):
    thread_id = threading.current_thread().ident
    text = race.text + " " + race.year
    if cause:
        text += " due to " + str(cause)

    get_logger().error(LOG_THREAD_FORMAT.format(thread_id, text, race.url))
