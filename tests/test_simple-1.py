
import os.path
from py.path import local
# from lxml import etree

from rng2doc.rng import create_intermediate, parserng

RNGFILE = local(__file__).dirpath("data") / "simple-1.rng"


def test_simple_1():
    root, rngtree = parserng(str(RNGFILE))
    result = create_intermediate(rngtree)

    assert result

