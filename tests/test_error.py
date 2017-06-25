# Third Party Libraries
import pytest

# My Stuff
from rng2doc.common import errorcode


def test_errorcode():
    assert errorcode(BaseException)  == 255
