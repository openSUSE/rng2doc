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

# Standard Library
import logging
import os
import sys
from logging.config import dictConfig

# Third Party Libraries
from docopt import DocoptExit, docopt, printable_usage

# Local imports
from . import __version__
from .common import DEFAULT_LOGGING_DICT, LOGLEVELS, errorcode
from .rng import process

#: Use __package__, not __name__ here to set overall logging level:
log = logging.getLogger(__package__)


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param cliargs: List of commandline arguments
    :type cliargs: list(str)
    :return: dictionary from :class:`docopt.docopt`
    :rtype: dict
    """
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__,
                  argv=cliargs, version=version)
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args['-v'], logging.DEBUG))

    return args


def checkargs(args):
    """Check arguments for validity

    :param args: parsed arguments from :class:`docopt.docopt`
    :type args: dict
    :raises: :class:`docopt.DocoptExit`, :class:`FileNotFoundError`
    :return:
    """
    rng = args['RNGFILE']
    if rng is None:
        raise DocoptExit()
    if not os.path.exists(rng):
        raise FileNotFoundError(rng)


def main(cliargs=None):
    """Entry point for the application script

    :param list(str) cliargs: Arguments to parse or None (=use ``sys.argv``)
    :return: return codes from :func:`rng2doc.common.errorcode`
    :rtype: int
    """

    try:
        args = parsecli(cliargs)
        log.info('%s version: %s', __package__, __version__)
        log.debug('Python version: %s', sys.version.split()[0])
        log.debug("CLI result: %s", args)
        checkargs(args)
        result = process(args)
        log.info("Done.")
        return result

    except DocoptExit as error:
        log.fatal("Need a RELAX NG file.")
        printable_usage(__doc__)
        return errorcode(error)

    except FileNotFoundError as error:
        log.fatal("File not found '%s'", error)
        return errorcode(error)

    except KeyboardInterrupt as error:
        return errorcode(error)
