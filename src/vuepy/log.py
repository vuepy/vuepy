import ipywidgets as widgets
import logging

from IPython.core.display_functions import display


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


out = widgets.Output()


def getLogger(name='vuepy', level=logging.INFO):
    handler = OutputWidgetHandler(out)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s  - [%(levelname)s] %(filename)s:%(lineno)s %(message)s'))

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
