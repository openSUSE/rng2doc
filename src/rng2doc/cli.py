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
    --output-format=<FORMAT>, -f <FORMAT>
                      Specifies the format of the output. (xml, html) [default: xml]
"""

# Standard Library
import logging
import os
import sys
from logging.config import dictConfig

# Third Party Libraries
from docopt import DocoptExit, docopt, printable_usage
from lxml import etree

# Local imports
from . import __version__
from .common import DEFAULT_LOGGING_DICT, LOGLEVELS, errorcode
from .rng import parse

#: Use __package__, not __name__ here to set overall LOGging level:
LOG = logging.getLogger(__package__)


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
    LOG.setLevel(LOGLEVELS.get(args['-v'], logging.DEBUG))

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
    oformat = args['--output-format'].lower()
    if oformat not in ('html', 'xml'):
        raise RuntimeError("Wrong format.")


def output(result, file_path, oformat):
    """Write the result to a file if the --output argument is set otherwise
       the result will be printed on stdout.

    :param result: The results of the transform method
    :type result: ElementTree
    :param file_path: The file path to the output file
    :type file_path: str
    :return: None
    """
    path, filename = os.path.split(file_path)
    if path != "":
        os.makedirs(path, exist_ok=True)
    if oformat == "html":
        path = os.path.join(path, "html")
        os.makedirs(os.path.join(path, "elements"), exist_ok=True)
        xslt_html = etree.parse("xslt/html.xslt")
        transform = etree.XSLT(xslt_html)
        result = transform(
            result, basedir="'{}'".format(path),
            filename="'{}'".format(filename))
    if file_path:
        result.write(
            os.path.join(path, filename), pretty_print=True, xml_declaration=True, encoding="utf-8")
    else:
        print(etree.tostring(result, pretty_print=True, encoding="unicode"))


def main(cliargs=None):
    """Entry point for the application script

    :param list(str) cliargs: Arguments to parse or None (=use ``sys.argv``)
    :return: return codes from :func:`rng2doc.common.errorcode`
    :rtype: int
    """
    try:
        args = parsecli(cliargs)
        LOG.info('%s version: %s', __package__, __version__)
        LOG.debug('Python version: %s', sys.version.split()[0])
        LOG.debug("CLI result: %s", args)
        checkargs(args)
        result = parse(args['RNGFILE'])
        output(result, args['--output'], args["--output-format"])
        LOG.info("Done.")
        return 0

    except DocoptExit as error:
        LOG.fatal("Need a RELAX NG file.")
        printable_usage(__doc__)
        return errorcode(error)

    except FileNotFoundError as error:
        LOG.fatal("File not found '%s'", error)
        return errorcode(error)

    except etree.XMLSyntaxError as error:
        LOG.fatal("Failed to parse the XML input file  '%s'", error)
        return errorcode(error)

    except RuntimeError as error:
        LOG.fatal("Something failed  '%s'", error)
        return 1

    except KeyboardInterrupt as error:
        return errorcode(error)
