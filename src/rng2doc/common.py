#
# Copyright (c) 2017 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

"""Constants for all the other modules
"""

# Third Party Libraries
from docopt import DocoptExit
from lxml.etree import QName, XMLSyntaxError

from logging import DEBUG, INFO, WARNING


# Error codes
# Make an error dictionary that contains both the class and its
# string representation
ERROR_CODES = dict()
for _error, _rc in [  # exception class, return value:
                    (XMLSyntaxError, 20),
                    (FileNotFoundError, 40),
                    (OSError, 40),
                    (DocoptExit, 50),
                    (KeyboardInterrupt, 200),
                    ]:
    ERROR_CODES[_error] = _rc
    ERROR_CODES[repr(_error)] = _rc


def errorcode(error):
    """Get the error exit code from an exception ``error``

    :param error: exception instance like :class:`OSError`
    :return: exit code
    :rtype: int
    """
    return ERROR_CODES.get(repr(type(error)), 255)


#: Prefix to namespace mappings
NSMAP = dict(a="http://relaxng.org/ns/compatibility/annotations/1.0",
             db="http://docbook.org/ns/docbook",
             html="http://www.w3.org/1999/xhtml",
             rng="http://relaxng.org/ns/structure/1.0",
             xlink="http://www.w3.org/1999/xlink",
             sch="http://purl.oclc.org/dsdl/schematron",
             xml="http://www.w3.org/XML/1998/namespace",
             )

# Relax NG namespace
RNG_GRAMMAR = QName(NSMAP['rng'], "grammar")
RNG_START = QName(NSMAP['rng'], "start")
RNG_INCLUDE = QName(NSMAP['rng'], "include")
RNG_DEFINE = QName(NSMAP['rng'], "define")
RNG_REF = QName(NSMAP['rng'], "ref")
RNG_EXTERNAL_REF = QName(NSMAP['rng'], "externalRef")
RNG_ELEMENT = QName(NSMAP['rng'], "element")
RNG_ATTRIBUTE = QName(NSMAP['rng'], "attribute")
RNG_ZERO_OR_MORE = QName(NSMAP['rng'], "zeroOrMore")
RNG_ONE_OR_MORE = QName(NSMAP['rng'], "oneOrMore")
RNG_LIST = QName(NSMAP['rng'], "list")
RNG_GROUP = QName(NSMAP['rng'], "group")
RNG_OPTIONAL = QName(NSMAP['rng'], "optional")
RNG_INTERLEAVE = QName(NSMAP['rng'], "interleave")
RNG_CHOICE = QName(NSMAP['rng'], "choice")
RNG_DATA = QName(NSMAP['rng'], "data")
RNG_TEXT = QName(NSMAP['rng'], "text")
RNG_EMPTY = QName(NSMAP['rng'], "empty")
RNG_PARAM = QName(NSMAP['rng'], "param")
RNG_VALUE = QName(NSMAP['rng'], "value")
RNG_ANY_NAME = QName(NSMAP['rng'], "anyName")
RNG_NS_NAME = QName(NSMAP['rng'], "nsName")
RNG_EXCEPT = QName(NSMAP['rng'], "except")
RNG_DIV = QName(NSMAP['rng'], "div")
RNG_MIXED = QName(NSMAP['rng'], "mixed")

# Docbook namespace
DB_PARA = QName(NSMAP['db'], "para")

# Schematron namespace
SCH_PATTERN = QName(NSMAP['sch'], "pattern")
SCH_PARAM = QName(NSMAP['sch'], "param")
SCH_RULE = QName(NSMAP['sch'], "rule")

A_DOC = QName(NSMAP['a'], "documentation")

#: Stylesheets
HTML_XSLT = "xslt/html.xslt"


#: Map verbosity to log levels
LOGLEVELS = {None: WARNING,  # 0
             0: WARNING,
             1: INFO,
             2: DEBUG,
             }
