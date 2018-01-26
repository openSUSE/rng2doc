"""Logging module

"""

# Standard Library
import logging

# Local imports
from .common import DEFAULT_LOGGING_DICT

#: the default logging format
DEFAULT_FORMAT = DEFAULT_LOGGING_DICT['formatters']['standard']['format']

#: a very simple format
SIMPLE_FORMAT = DEFAULT_LOGGING_DICT['formatters']['myformatter']['format']


class CustomConsoleFormatter(logging.Formatter):
    """
    Modify the way DEBUG messages are displayed.
    """
    # Lists all different formats
    FORMATS = {logging.INFO: logging.Formatter(SIMPLE_FORMAT),
               logging.WARNING: logging.Formatter(SIMPLE_FORMAT),
               logging.ERROR: logging.Formatter(SIMPLE_FORMAT),
               logging.FATAL: logging.Formatter(SIMPLE_FORMAT),
               'DEFAULT': logging.Formatter(DEFAULT_FORMAT),
               }

    def format(self, record):
        "Format the specified record as text."
        fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        return fmt.format(record)
