# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
import logging

from vuepy.reactivity import config

LOGGER_NAME = 'vuepy'
LOGGER_FORMATTER = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s:%(funcName)s - %(message)s'
)


def getLogger(name=LOGGER_NAME):
    return logging.getLogger(name)


def add_handler(handler):
    logger = getLogger(LOGGER_NAME)
    handler.setFormatter(LOGGER_FORMATTER)
    logger.addHandler(handler)


def init():
    logger = getLogger(LOGGER_NAME)
    logger.setLevel(config.LOG_LEVEL)
    logger.propagate = False


init()
