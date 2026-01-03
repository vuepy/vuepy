# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from textual.logging import TextualHandler

from vuepy import log
from textual_vuepy.comps import *

logger = log.getLogger()

textual_handler = TextualHandler()
textual_handler.setFormatter(log.LOGGER_FORMATTER)

logger.addHandler(textual_handler)
