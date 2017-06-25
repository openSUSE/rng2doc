# Standard Library
from unittest.mock import patch

# Third Party Libraries
import pytest
from lxml import etree

# My Stuff
from rng2doc.exceptions import NoMatchinRootException
from rng2doc.rng import parserng


@patch('rng2doc.rng.etree.parse')
def test_parserng(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""<wrongelement xmlns="urn:x-test:wrong-ns"/>""").getroottree()

    mock_parse.side_effect = xmltree
    with pytest.raises(NoMatchinRootException):
        parserng("fake.rng")
