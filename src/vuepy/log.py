import logging

import ipywidgets as widgets
from IPython.core.display_functions import display

from vuepy.reactivity import config

LOGGER_NAME = 'vuepy'
logout = widgets.Output()


class OutputWidgetHandler(logging.Handler):
    """ Custom logging handler sending logs to an output widget """

    def __init__(self, out, *args, **kwargs):
        super(OutputWidgetHandler, self).__init__(*args, **kwargs)
        self.out = out

    def emit(self, record):
        """ Overload of logging.Handler method """
        formatted_record = self.format(record)
        new_output = {
            'name': 'stdout',
            'output_type': 'stream',
            'text': formatted_record + '\n'
        }
        self.out.outputs = (new_output,) + self.out.outputs

    def show_logs(self):
        """ Show the logs """
        display(self.out)

    def clear_logs(self):
        """ Clear the current logs """
        self.out.clear_output()


def getLogger(name=LOGGER_NAME):
    return logging.getLogger(name)


def init():
    handler = OutputWidgetHandler(logout)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(filename)s:%(funcName)s:%(lineno)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger = getLogger(LOGGER_NAME)
    logger.addHandler(handler)
    logger.setLevel(config.LOG_LEVEL)


init()
