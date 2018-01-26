"""
Exceptions
"""


class RNGBaseException(Exception):
    """
    Base exception for all rng2doc related errors
    """
    pass


class NoMatchinRootException(RNGBaseException):
    """
    Raised when the root element is not a valid element from
    the RELAX NG namespace or if the root element is not
    allowed according to the RELAX NG spec
    """
    pass
