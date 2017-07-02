# Standard Library
from io import StringIO
from unittest.mock import patch

# Third Party Libraries
import pytest
from lxml import etree

# My Stuff
from rng2doc.exceptions import NoMatchingRootException
from rng2doc.common import NSMAP
from rng2doc.rng import parserng, process


@patch('rng2doc.rng.etree.parse')
def test_parserng(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""<wrongelement xmlns="urn:x-test:wrong-ns"/>""").getroottree()

    mock_parse.side_effect = xmltree
    with pytest.raises(NoMatchingRootException):
        parserng("fake.rng")


@patch('rng2doc.rng.etree.parse')
def test_parserng_element(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""<element name="foo"
         xmlns="http://relaxng.org/ns/structure/1.0"/>""").getroottree()

    rng_element = etree.QName(NSMAP['rng'], "element").text
    mock_parse.side_effect = xmltree
    root, tree = parserng("fake.rng")
    assert root.text == rng_element
    assert tree.getroot().tag == rng_element


def test_parserng_element_with_stringio():
    fh = StringIO("""<element name="foo"
         xmlns="http://relaxng.org/ns/structure/1.0"/>""")
    rng_element = etree.QName(NSMAP['rng'], "element").text
    root, tree = parserng(fh)
    assert root.text == rng_element
    assert tree.getroot().tag == rng_element


@patch('rng2doc.rng.etree.parse')
def test_process_with_success(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""<element name="foo"
         xmlns="http://relaxng.org/ns/structure/1.0"><empty/></element>""").getroottree()

    mock_parse.side_effect = xmltree
    result = process({'RNGFILE': 'fake.rng'})
    assert result == 0
