"""Converts RELAX NG schema into documentation

Usage:
    rng2doc [-h | --help]
    rng2doc [-v ...] [options] RNGFILE

Required Arguments:
    RNGFILE          Path to RELAX NG file (file extension .rng)

Options:
    -h, --help        Shows this help
    -v                Raise verbosity level
    --version         Prints the version
    --output=<OUTFILE>, -o <OUTFILE>
                      Optional file where results are written to
"""

from .common import (DEFAULT_LOGGING_DICT,
                     LOGLEVELS,
                     )

from docopt import docopt, DocoptExit
import logging
from logging.config import dictConfig
import sys

#: Use __package__, not __name__ here to set overall logging level:
log = logging.getLogger(__package__)


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param list cliargs: List of commandline arguments
    :return: dictionary from docopt
    :rtype: dict
    """
    from rng2doc import __version__
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__,
                  argv=cliargs, version=version)
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args['-v'], logging.DEBUG))

    log.debug("CLI result: %s", args)
    log.warning("Huhu!")
    return args


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: return codes from ``ERROR_CODES``
    """

    try:
        args = parsecli(cliargs)
        # checkargs(args)
        result = 0 # process(args)
        log.info("Done.")
        return result

    except KeyboardInterrupt:
        return 10


def __main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """

    print(argv)
    return 0
