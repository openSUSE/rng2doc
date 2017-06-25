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

# Third Party Libraries
from docopt import DocoptExit
from lxml.etree import QName, XMLSyntaxError

from logging import (CRITICAL,  # isort:skip
                     DEBUG,
                     ERROR,
                     FATAL,
                     INFO,
                     NOTSET,
                     WARN,
                     WARNING,
                     )


# Error codes
# Make an error dictionary that contains both the class and its
# string representation
ERROR_CODES = dict()
for _error, _rc in [(XMLSyntaxError, 20),
                    (FileNotFoundError, 40),
                    (OSError, 40),
                    (DocoptExit, 50),
                    (KeyboardInterrupt, 200),
                    ]:
    ERROR_CODES[_error] = _rc
    ERROR_CODES[repr(_error)] = _rc


def errorcode(error):
    """Get the error exit code from an exception ``error``

    :param error: exception instance
    :return: exit code
    :rtype: int
    """
    return ERROR_CODES.get(repr(type(error)), 255)


#: Prefix to namespace mappings
NSMAP = dict(a="http://relaxng.org/ns/compatibility/annotations/1.0",
             db="http://docbook.org/ns/docbook",
             html="http://www.w3.org/1999/xhtml",
             rng="http://relaxng.org/ns/structure/1.0",
             s="http://purl.oclc.org/dsdl/schematron",
             xlink="http://www.w3.org/1999/xlink"
             )

#: Some RNG elements
RNG_ELEMENT = QName(NSMAP['rng'], "element")
RNG_ATTRIBUTE = QName(NSMAP['rng'], "attribute")
RNG_REF = QName(NSMAP['rng'], "ref")
# DEFVALUE = QName(NSMAP['a'], "defaultValue")

#: Map verbosity to log levels
LOGLEVELS = {None: WARNING,  # 0
             0: WARNING,
             1: INFO,
             2: DEBUG,
             }

#: Map log numbers to log names
LOGNAMES = {NOTSET: 'NOTSET',      # 0
            None: 'NOTSET',
            DEBUG: 'DEBUG',        # 10
            INFO: 'INFO',          # 20
            WARN: 'WARNING',       # 30
            WARNING: 'WARNING',    # 30
            ERROR: 'ERROR',        # 40
            CRITICAL: 'CRITICAL',  # 50
            FATAL: 'CRITICAL',     # 50
            }

#: Default logging dict for :class:`logging.config.dictConfig`:
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            # See https://docs.python.org/3.5/library/logging.html#logrecord-attributes
            'format': '[%(levelname)s] %(name)s::%(funcName)s: %(message)s'
        },
        'myformatter': {
            '()': 'rng2doc.log.CustomConsoleFormatter',
            'format': '[%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stderr',
            },
        'myhandler': {
            'level': 'NOTSET',
            'formatter': 'myformatter',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stderr',
            },
    },
    'loggers': {
        'rng2doc': {
            'handlers': ['myhandler', ],  # 'default'
            'level': 'INFO',
            'propagate': True
        }
    }
}
