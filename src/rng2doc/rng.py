"""

"""

# Standard Library
import logging
from collections import OrderedDict

# Third Party Libraries
from lxml import etree

# Local imports
from .common import NSMAP, RNG_NS, RNG_DOCUMENTATION_TAG, RNG_ELEMENT_TAG
from .exceptions import NoMatchingRootException

log = logging.getLogger(__name__)

#  gh://openSUSE/xmldiffng:xmldiffng/contrib/parse-rng.py


def parserng(source, xmlparser=None):
    """Read RNG source and return a tuple of its root element and the RNG tree

     :param source: The ``source`` can be any of the following:
        * a file name/path
        * a file object
        * a file-like object
        * a URL using the HTTP or FTP protocol
     :type source: str | file | file_like | URL
     :param xmlparser: used XMLParser (default to None)
     :type xmlparser: :class:`lxml.etree.XMLParser`
     :return: root element and parsed RNG tree
     :rtype: tuple
    """
    rngtree = etree.parse(source, xmlparser)

    root = etree.QName(rngtree.getroot())
    if root.namespace != RNG_NS:
        raise NoMatchingRootException("Wrong namespace in root element %s. "
                                     "Expected RELAX NG namespace" % root.text)
    # TODO: Validate tree with RNG schema
    # TODO: Check for missing defines and refs (see missing-defs.xsl)
    return root, rngtree


def rngdocumentation(element):
    """Find documentation from element node

    :param element: element node to check for documentation
    :type element: :class:`lxml.etree._Element`
    :return: None or element node
    :rtype: None | :class:`lxml.etree._Element`
    """
    doc_element = RNG_DOCUMENTATION_TAG.text
    doc = element.find(doc_element)

    return doc if doc is None else doc.text


def rngelement(element):
    """Find an element from the tree

    :param rngtree:
    :type rngtree: :class:`lxml.etree._ElementTree`
    :return: None or dict
    """
    rng_element = RNG_ELEMENT_TAG
    name = element.attrib.get('name')
    doc = rngdocumentation(element)

    return {name: {'doc': doc},
                  # {'attrib'. attrib},
                  # {'children': None},
            }


def create_intermediate(rngtree):
    """Transform RNG tree into intermediate structure for easier handling

    :param rngtree:
    :return:
    """
    root = etree.QName(rngtree.getroot())
    start = {'element': rngelement,
             # 'attribte'. rngattribute,
             # 'grammar': rnggrammar,
             }
    func = start.get(root.localname)
    result = func(rngtree.getroot())
    return result


def process(args):
    """Process RELAX NG file

    :param args: result dictionary from docopt
    :return:
    """
    log.info("Process RNG file...")
    root, rngtree = parserng(args['RNGFILE'])
    result = create_intermediate(rngtree)

    print(root.text, result)
    return 0
