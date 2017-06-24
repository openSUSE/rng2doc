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
                     errorcode,
                     )

from docopt import docopt, DocoptExit, printable_usage
import logging
from logging.config import dictConfig
import os

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
    return args


def checkargs(args):
    """Check arguments for validity

    :param args:
    :return:
    """
    rng = args['RNGFILE']
    if rng is None:
        raise DocoptExit()
    if not os.path.exists(rng):
        raise FileNotFoundError(rng)


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: return codes from ``ERROR_CODES``
    """

    try:
        args = parsecli(cliargs)
        checkargs(args)
        result = 0 # process(args)
        log.info("Done.")
        return result

    except DocoptExit as error:
        log.fatal("Need a RELAX NG file.")
        printable_usage(__doc__)
        return 10

    except FileNotFoundError as error:
        log.fatal("File not found '%s'", error)
        return errorcode(error)

    except KeyboardInterrupt:
        return 10
