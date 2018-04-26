# Standard Library
import io
from functools import partial
from unittest.mock import patch

# Third Party Libraries
import pytest
from lxml import etree

# My Stuff
from rng2doc.exceptions import NoMatchinRootException
from rng2doc.rng import process, transform

PARSER = etree.XMLParser(remove_blank_text=True)

@patch('rng2doc.rng.etree.parse')
def test_transform(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""""").getroottree()

    mock_parse.side_effect = xmltree
    with pytest.raises(XMLSyntaxError):
        transform("fake.rng")

@patch('rng2doc.rng.etree.parse')
def test_transform(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""<wrongelement xmlns="urn:x-test:wrong-ns"/>""").getroottree()

    mock_parse.side_effect = xmltree
    with pytest.raises(NoMatchinRootException):
        transform("fake.rng")

@pytest.mark.parametrize('xml,expected', [
    ("""<element name="foo" xmlns="http://relaxng.org/ns/structure/1.0"/>""",
     """<documentation>
          <element name="foo">
            <namespace/>
            <description/>
          </element>
        </documentation>"""
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0"><start><element name="foo"/></start></grammar>""",
     """<documentation>
          <element name="foo">
            <namespace/>
            <description></description>
          </element>
        </documentation>"""
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0"><element name="foo"></element></element>""", 
     """<documentation>
          <element name="root">
            <namespace/>
            <description/>
            <child id="foo"/>
          </element>
          <element name="foo">
            <namespace/>
            <description/>
          </element>
        </documentation>"""
 
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
          <element name="foo"></element>
          <element name="bar"></element>
        </element>""", 
     """<documentation>
          <element name="root">
            <namespace/>
            <description/>
            <child id="foo"/>
            <child id="bar"/>
          </element>
          <element name="foo">
            <namespace/>
            <description/>
          </element>
          <element name="bar">
            <namespace/>
            <description/>
          </element>
        </documentation>"""
    )
])
def test_transform_element(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)

@pytest.mark.parametrize('xml,expected', [
    ("""<element name="foo" xmlns="http://relaxng.org/ns/structure/1.0">
        <attribute name="test"><text/></attribute>
      </element>""",
     """<documentation>
          <element name="foo">
            <namespace/>
            <description/>
            <attribute>
              <name>test</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>required</use>
            </attribute>
          </element>
        </documentation>"""
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
          <attribute name="test"><text/></attribute>
          <attribute name="test2"><text/></attribute>
          <element name="foo">
            <attribute name="test3"><text/></attribute>
          </element>
        </element>""",
     """<documentation>
          <element name="root">
            <namespace/>
            <description/>
            <child id="foo"/>
            <attribute>
              <name>test</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>required</use>
            </attribute>
            <attribute>
              <name>test2</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>required</use>
            </attribute>
          </element>
          <element name="foo">
            <namespace/>
            <description/>
            <attribute>
              <name>test3</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>required</use>
            </attribute>
          </element>
        </documentation>"""
    ),
])
def test_transform_attribute(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)

@pytest.mark.parametrize('xml,expected', [
    ("""<element name="foo" xmlns="http://relaxng.org/ns/structure/1.0">
          <optional>
            <attribute name="test"><text/></attribute>
          </optional>
        </element>""",
     """<documentation>
          <element name="foo">
            <namespace/>
            <description/>
            <attribute>
              <name>test</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>optional</use>
            </attribute>
          </element>
        </documentation>"""
    ),
    ("""<element name="foo" xmlns="http://relaxng.org/ns/structure/1.0">
          <attribute name="test"><text/></attribute>
        </element>""",
     """<documentation>
          <element name="foo">
            <namespace/>
            <description/>
            <attribute>
              <name>test</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>required</use>
            </attribute>
          </element>
        </documentation>"""
    ),
])
def test_transform_optional(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)


@pytest.mark.parametrize('xml,expected', [
    ("""<element name="foo" xmlns="http://relaxng.org/ns/structure/1.0" xmlns:a="http://relaxng.org/ns/compatibility/annotations/1.0">
          <a:documentation>This is a test element.</a:documentation>
          <optional>
            <attribute name="test">
              <a:documentation>This is a test attribute.</a:documentation>
              <text/>
            </attribute>
          </optional>
        </element>""",
     """<documentation>
          <element name="foo">
            <namespace/>
            <description>This is a test element.</description>
            <attribute>
              <name>test</name>
              <namespace/>
              <description>This is a test attribute.</description>
              <type>text</type>
              <use>optional</use>
            </attribute>
          </element>
        </documentation>"""
    ),
])
def test_transform_annotations(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)


@pytest.mark.parametrize('xml,expected', [
    ("""<element name="test" xmlns="http://relaxng.org/ns/structure/1.0">
            <attribute name="test_attribute">
              <data type="string"/>
            </attribute>
        </element>""",
     """<documentation>
          <element name="test">
            <namespace/>
            <description/>
            <attribute>
              <name>test_attribute</name>
              <namespace/>
              <description/>
              <type>string</type>
              <use>required</use>
            </attribute>
          </element>
        </documentation>"""
    ),
])
def test_transform_datatype(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)


@pytest.mark.parametrize('xml,expected', [
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <element name="test">
              <zeroOrMore>
                <element name="subtest">
                  <ref name="subtest.attlist"/>
                </element>
              </zeroOrMore>
            </element>
          </start>

          <define name="subtest.attlist">
            <interleave>
              <attribute name="test_attribute1">
                <text/>
              </attribute>
              <attribute name="test_attribute2">
                <text/>
              </attribute>
            </interleave>
          </define>
        </grammar>""",
     """<documentation>
          <element name="test">
            <namespace/>
            <description></description>
            <child id="subtest"/>
          </element>
          <element name="subtest">
            <namespace/>
            <description></description>
            <attribute>
              <name>test_attribute1</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>required</use>
            </attribute>
            <attribute>
              <name>test_attribute2</name>
              <namespace/>
              <description/>
              <type>text</type>
              <use>required</use>
            </attribute>
          </element>
        </documentation>"""
    ),
])
def test_transform_references(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)


@pytest.mark.parametrize('xml,expected', [
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <element name="test">
              <zeroOrMore>
                <element name="subtest">
                  <ref name="subtest.attlist"/>
                </element>
              </zeroOrMore>
            </element>
          </start>

          <define name="subtest.attlist">
            <attribute name="test_attribute1">
              <choice>
                <value>value1</value>
                <value>value2</value>
              </choice>
            </attribute>
          </define>
        </grammar>""",
     """<documentation>
          <element name="test">
            <namespace/>
            <description></description>
            <child id="subtest"/>
          </element>
          <element name="subtest">
            <namespace/>
            <description></description>
            <attribute>
              <name>test_attribute1</name>
              <namespace/>
              <description/>
              <type>enum [value1|value2]</type>
              <use>required</use>
            </attribute>           
          </element>
        </documentation>"""
    ),
])
def test_transform_enumerations(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)


@pytest.mark.parametrize('xml,expected', [
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <ref name="anyElement"/>
          </start>

          <define name="anyElement">
            <element>
              <anyName/>
              <zeroOrMore>
                <choice>
                  <attribute>
                    <anyName/>
                  </attribute>
                  <text/>
                  <ref name="anyElement"/>
                </choice>
              </zeroOrMore>
            </element>
          </define>
        </grammar>""",
     """<documentation>
          <element name="anyElement">
            <namespace/>
            <description/>
            <child id="anyElement"/>
            <attribute>
              <name/>
              <namespace/>
              <description/>
              <type/>
              <use>required</use>
            </attribute>
          </element>
        </documentation>"""
    ),
])
def test_transform_name_classes(xml, expected):
    result = transform(io.StringIO(xml))
    expected_tree = etree.fromstring(expected, parser=PARSER)
    assert isinstance(result, etree._ElementTree)
    assert etree.tostring(result) == etree.tostring(expected_tree)
