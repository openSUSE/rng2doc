"""

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
    """Read RNG file and return a dictionary in the format of
       { 'element': [ (name1, value1), ...], }

     :param rngfilename: path to the RNG file (in XML format)
     :type rngfilename: str
     :return: result dictionary
     :rtype: dict
    """
    xmlparser = None
    rngtree = etree.parse(rngfilename, xmlparser)

    root = etree.QName(rngtree.getroot())
    if root.namespace != NSMAP['rng']:
        raise NoMatchinRootException("Wrong namespace in root element %s. "
                                     "Expected namespace from RELAX NG" % root.text)

    # Maybe there is a more efficient method:
    rngelements = rngtree.xpath("//rng:define[rng:element]|/rng:element", namespaces=NSMAP)
    alldefines = rngtree.xpath("//rng:define[not(rng:element)]", namespaces=NSMAP)
    definedict = {node.attrib['name']: node for node in alldefines}
    result = OrderedDict()

    return result


def process(args):
    """Process RELAX NG file

    :param args: result dictionary from docopt
    :return:
    """
    log.info("Process RNG file...")
    result = parserng(args['RNGFILE'])
    print(result)
    return 0
