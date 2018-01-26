"""Parsing RNG file and creating intermediate structure

"""

# Standard Library
import logging
from collections import OrderedDict

# Third Party Libraries
from lxml import etree

# Local imports
from .common import NSMAP
from .exceptions import NoMatchinRootException

log = logging.getLogger(__name__)

#  gh://openSUSE/xmldiffng:xmldiffng/contrib/parse-rng.py


def parserng(rngfilename, elementdef=None):
    """Read RNG file and return a dictionary in the format of::

      { 'element': [ (name1, value1), ...], }

     :param rngfilename: path to the RNG file (in XML format)
     :type rngfilename: str
     :return: result dictionary
     :rtype: dict(str, list(str, ...))
    """
    xmlparser = None
    rngtree = etree.parse(rngfilename, xmlparser)

    root = etree.QName(rngtree.getroot())
    if root.namespace != NSMAP['rng']:
        raise NoMatchinRootException("Wrong namespace in root element %s. "
                                     "Expected namespace from RELAX NG" % root.text)
    # FIXME: Add something usefule here:
    result = OrderedDict()
    return result


def process(args):
    """Process RELAX NG file

    :param args: result dictionary from :class:`docopt.docopt`
    :return: result dictionary
    :rtype: dict
    """
    rngfile = args['RNGFILE']
    log.info("Process RNG file %r...", rngfile)
    result = parserng(rngfile)
    print(result)
    return 0
