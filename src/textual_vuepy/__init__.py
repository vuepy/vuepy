# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from textual.logging import TextualHandler

from vuepy import log
from textual_vuepy.comps import *

log.add_handler(TextualHandler())
