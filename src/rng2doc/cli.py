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
    --timing          Output timing data to standard error
                      perf:  It does include time elapsed during sleep and is
                             system-wide.
                      proc:  It does not include time elapsed during sleep.
    --output=<OUTFILE>, -o <OUTFILE>
                      Optional file where results are written to
    --output-format=<FORMAT>, -f <FORMAT>
                      Specifies the format of the output. (xml, html) [default: xml]
"""

# Standard Library
import os
import logging
import sys
import time
from pkg_resources import resource_filename

# Third Party Libraries
from docopt import DocoptExit, docopt, printable_usage
from lxml import etree

# Local imports
from . import __version__
from .log import setup_logging
from .common import LOGLEVELS, errorcode
from .rng import parse


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
        xslt_html = etree.parse(resource_filename(__package__, "xslt/html.xslt"))
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
        logger = setup_logging(LOGLEVELS.get(args['-v'], logging.DEBUG))
        if args['--timing']:
            t_perf = time.perf_counter()
            t_proc = time.process_time()
        logger.info('%s version: %s', __package__, __version__)
        logger.debug('Python version: %s', sys.version.split()[0])
        logger.debug("CLI result: %s", args)
        checkargs(args)
        result = parse(args['RNGFILE'])
        output(result, args['--output'], args["--output-format"])
        if args['--timing']:
            elapsed_time_perf = time.perf_counter() - t_perf
            elapsed_time_proc = time.process_time() - t_proc
            timing_msg = "{:7} (timing): {} perf, {} proc"
            timing_msg = timing_msg.format(__package__, elapsed_time_perf, elapsed_time_proc)
            print(timing_msg, file=sys.stderr)
        logger.info("Done.")
        return 0

    except DocoptExit as error:
        logger.fatal("Need a RELAX NG file.")
        printable_usage(__doc__)
        return errorcode(error)

    except FileNotFoundError as error:
        logger.fatal("File not found '%s'", error)
        return errorcode(error)

    except etree.XMLSyntaxError as error:
        logger.fatal("Failed to parse the XML input file  '%s'", error)
        return errorcode(error)

    except RuntimeError as error:
        logger.fatal("Something failed  '%s'", error)
        return 1

    except KeyboardInterrupt as error:
        return errorcode(error)
