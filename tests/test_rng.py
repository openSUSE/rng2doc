# Standard Library
import io
from unittest.mock import patch

# Third Party Libraries
import pytest
from lxml import etree
from lxml.etree import RelaxNGParseError, XMLSyntaxError

# My Stuff
from rng2doc.exceptions import NoMatchinRootException
from rng2doc.rng import parse, transform

PARSER = etree.XMLParser(remove_blank_text=True)

@patch('rng2doc.rng.etree.parse')
def test_parse_empty(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""""").getroottree()

    mock_parse.side_effect = xmltree
    with pytest.raises(XMLSyntaxError):
        parse("fake.rng")

@patch('rng2doc.rng.etree.parse')
def test_parse(mock_parse):
    def xmltree(source, parser=None, base_url=None):
        return etree.XML("""<wrongelement xmlns="urn:x-test:wrong-ns"/>""").getroottree()

    mock_parse.side_effect = xmltree
    with pytest.raises(RelaxNGParseError):
        parse("fake.rng")

@pytest.mark.parametrize('xml,expected', [
    ("""<element name="test" xmlns="http://relaxng.org/ns/structure/1.0"><text/></element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="test">
     #     <namespace/>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("count(//element)", 1),
         ("boolean(//element/namespace)", True),
         ("boolean(/documentation/element[@name = 'test'])", True),
     ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <element name="test">
              <text/>
            </element>
          </start>
        </grammar>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #  <element name="test">
     #    <namespace/>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("count(//element)", 1),
         ("boolean(//element/namespace)", True),
         ("boolean(/documentation/element[@name = 'test'])", True),
     ]
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
          <element name="test">
            <text/>
          </element>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element id="0" name="root">
     #     <namespace/>
     #     <child id="1"/>
     #   </element>
     #   <element id="1" name="test">
     #     <namespace/>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("count(//element)", 2),
         ("boolean(//element/namespace)", True),
         ("boolean(/documentation/element[@name = 'root'])", True),
         ("boolean(/documentation/element[@name = 'root']/child[@id = '1'])", True),
         ("boolean(/documentation/element[@name = 'test'])", True),
     ]

    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
          <element name="test1"><text/></element>
          <element name="test2"><text/></element>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element id='0' name="root">
     #     <namespace/>
     #     <child id="1"/>
     #     <child id="2"/>
     #   </element>
     #   <element id='1' name="test1">
     #     <namespace/>
     #   </element>
     #   <element id='2' name="test2">
     #     <namespace/>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("count(//element)", 3),
         ("boolean(//element/namespace)", True),
         ("boolean(/documentation/element[@name = 'root'])", True),
         ("boolean(/documentation/element[@name = 'root']/child[@id = '1'])", True),
         ("boolean(/documentation/element[@name = 'root']/child[@id = '2'])", True),
         ("boolean(/documentation/element[@name = 'test1'])", True),
         ("boolean(/documentation/element[@name = 'test2'])", True),
     ]
    )
])
def test_transform_element(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value

@pytest.mark.parametrize('xml,expected', [
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
        <attribute name="test"><text/></attribute>
      </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root">
     #     <namespace/>
     #     <attribute name="test">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("boolean(//attribute/namespace)", True),
         ("boolean(//attribute[@name = 'test'])", True),
         ("boolean(//attribute/type)", True),
         ("boolean(//attribute/type[@name = 'text'])", True),
         ("boolean(//attribute/use)", True),
         ("count(/documentation/element[@name = 'root']/attribute)", 1),
     ]
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
          <attribute name="test1"><text/></attribute>
          <attribute name="test2"><text/></attribute>
          <element name="element1">
            <attribute name="test3"><text/></attribute>
          </element>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root" id="0">
     #     <namespace/>
     #     <child id="1"/>
     #     <attribute name="test">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>required</use>
     #     </attribute>
     #     <attribute name="test2">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     #   <element name="element1" id="1">
     #     <namespace/>
     #     <attribute name="test3">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("boolean(//attribute/namespace)", True),
         ("boolean(//attribute/type)", True),
         ("boolean(//attribute/use)", True),
         ("count(/documentation/element[@name = 'root']/attribute)", 2),
         ("count(/documentation/element[@name = 'element1']/attribute)", 1),
         ("boolean(/documentation/element[@name = 'root']/attribute[@name = 'test1'])",
           True),
         ("boolean(/documentation/element[@name = 'root']/attribute[@name = 'test2'])",
           True),
         ("boolean(/documentation/element[@name = 'element1']/attribute[@name = 'test3'])",
           True),
     ]
    ),
])
def test_transform_attribute(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value

@pytest.mark.parametrize('xml,expected', [
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
          <optional>
            <attribute name="test"><text/></attribute>
          </optional>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root">
     #     <namespace/>
     #     <attribute name="test">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>optional</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("count(/documentation/element[@name = 'root']/attribute)", 1),
         ("boolean(/documentation/element[@name = 'root']/attribute[@name = 'test'])",
           True),
         ("/documentation/element[@name = 'root']/attribute[1]/use/text()",
          ["optional"]),
     ]
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
          <attribute name="test"><text/></attribute>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root">
     #     <namespace/>
     #     <attribute name="test">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("count(/documentation/element[@name = 'root']/attribute)", 1),
         ("boolean(/documentation/element[@name = 'root']/attribute[@name = 'test'])",
           True),
         ("/documentation/element[@name = 'root']/attribute[1]/use/text()",
          ["required"]),
     ]
    ),
])
def test_transform_optional(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value


@pytest.mark.parametrize('xml,expected', [
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0"
         xmlns:a="http://relaxng.org/ns/compatibility/annotations/1.0">
          <a:documentation>This is a test element.</a:documentation>
          <optional>
            <attribute name="test">
              <a:documentation>This is a test attribute.</a:documentation>
              <text/>
            </attribute>
          </optional>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root">
     #     <namespace/>
     #     <description>This is a test element.</description>
     #     <attribute name="test">
     #       <namespace/>
     #       <description>This is a test attribute.</description>
     #       <type name="text"/>
     #       <use>optional</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("/documentation/element[@name = 'root']/description/text()",
          ["This is a test element."]),
         ("/documentation/element[@name = 'root']/attribute/description/text()",
          ["This is a test attribute."]),
     ]
    ),
])
def test_transform_annotations(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value


@pytest.mark.parametrize('xml,expected', [
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
            <attribute name="test">
              <data type="string"/>
            </attribute>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root" id="0">
     #     <namespace/>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type name="string"/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("boolean(/documentation/element[@name = 'root']/attribute/type[@name = 'string'])", True),
     ]
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0">
            <attribute name="test">
              <data type="token">
                <param name="pattern">[a-zA-Z0-9_\-\.]+</param>
              </data>
            </attribute>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root">
     #     <namespace/>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type name="token">
     #         <param name="pattern">[a-zA-Z0-9_\-\.]+</param>
     #       </type>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("boolean(/documentation/element[@name = 'root']/attribute/type[@name = 'token'])", True),
         ("boolean(/documentation/element[@name = 'root']/attribute/type[@name = 'token']/param[@name = 'pattern'])", True),
         ("/documentation/element[@name = 'root']/attribute/type[@name = 'token']/param[@name = 'pattern']/text()",
          ["[a-zA-Z0-9_\-\.]+"]),
     ]
    ),
    ("""<element name="root" xmlns="http://relaxng.org/ns/structure/1.0"
         xmlns:a="http://relaxng.org/ns/compatibility/annotations/1.0">
            <attribute name="test">
              <data type="string">
                <a:documentation>This is a test datatype</a:documentation>
              </data>
            </attribute>
        </element>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="root">
     #     <namespace/>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type name="string">
     #         <description>This is a test datatype</description>
     #       </type>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("/documentation/element[@name = 'root']/attribute/type/description/text()",
          ["This is a test datatype"]),
     ]
    ),
])
def test_transform_datatype(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value


@pytest.mark.parametrize('xml,expected', [
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <element name="test1">
              <zeroOrMore>
                <element name="test2">
                  <ref name="test2.attlist"/>
                </element>
              </zeroOrMore>
            </element>
          </start>

          <define name="test2.attlist">
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
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="test1">
     #     <namespace/>
     #     <child id="test2"/>
     #   </element>
     #   <element name="test2">
     #     <namespace/>
     #     <attribute name="test_attribute1">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>required</use>
     #     </attribute>
     #     <attribute name="test_attribute2">
     #       <namespace/>
     #       <type name="text"/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>"""
     [
         ("local-name(/*)", "documentation"),
         ("count(/documentation/element)", 2),
         ("count(/documentation/element[@name = 'test2']/attribute)", 2),
         ("boolean(/documentation/element[@name = 'test2']/attribute[@name = 'test_attribute1'])",
           True),
         ("boolean(/documentation/element[@name = 'test2']/attribute[@name = 'test_attribute2'])",
           True),
     ]

    ),
])
def test_transform_references(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value


@pytest.mark.parametrize('xml,expected', [
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <element name="test1">
              <zeroOrMore>
                <element name="test2">
                  <ref name="test2.attlist"/>
                </element>
              </zeroOrMore>
            </element>
          </start>

          <define name="test2.attlist">
            <attribute name="test_attribute1">
              <choice>
                <value>value1</value>
                <value>value2</value>
              </choice>
            </attribute>
          </define>
        </grammar>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="test1" id="0">
     #     <namespace/>
     #     <child id="test2"/>
     #   </element>
     #   <element name="test2" id="1">
     #     <namespace/>
     #     <attribute name="test_attribute1">
     #       <namespace/>
     #       <type name="enum">
     #         <value name="value1"/>
     #         <value name="value2"/>
     #       </type>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>"""
     [
         ("local-name(/*)", "documentation"),
         ("boolean(/documentation/element[@name = 'test2']/attribute[1]/type[@name = 'enum'])", True),
         ("boolean(/documentation/element[@name = 'test2']/attribute[1]/type/value[@name = 'value1'])", True),
         ("boolean(/documentation/element[@name = 'test2']/attribute[1]/type/value[@name = 'value2'])", True),
     ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0"
         xmlns:a="http://relaxng.org/ns/compatibility/annotations/1.0">
          <start>
            <element name="test1">
              <zeroOrMore>
                <element name="test2">
                  <ref name="test2.attlist"/>
                </element>
              </zeroOrMore>
            </element>
          </start>

          <define name="test2.attlist">
            <attribute name="test_attribute1">
              <choice>
                <value>value1</value>
                <a:documentation>A test value1</a:documentation>
                <value>value2</value>
                <a:documentation>A test value2</a:documentation>
              </choice>
            </attribute>
          </define>
        </grammar>""",
     # The expected result looks like:
     # -------------------------------
     # <documentation>
     #   <element name="test1">
     #     <namespace/>
     #     <child id="test2"/>
     #   </element>
     #   <element name="test2">
     #     <namespace/>
     #     <attribute name="test_attribute1">
     #       <namespace/>
     #       <type name="enum">
     #         <value name="value1">
     #            <description>A test value1</description>
     #         </value>
     #         <value name="value2">
     #            <description>A test value2</description>
     #         </value>
     #       </type>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>"""
     [
         ("local-name(/*)", "documentation"),
         ("boolean(/documentation/element[@name = 'test2']/attribute[1]/type[@name = 'enum'])", True),
         ("boolean(/documentation/element[@name = 'test2']/attribute[1]/type/value[@name = 'value1'])", True),
         ("/documentation/element[@name = 'test2']/attribute[1]/type/value[@name = 'value1']/description/text()",
           ["A test value1"]),
         ("boolean(/documentation/element[@name = 'test2']/attribute[1]/type/value[@name = 'value2'])", True),
         ("/documentation/element[@name = 'test2']/attribute[1]/type/value[@name = 'value2']/description/text()",
           ["A test value2"]),
     ]
    ),
])
def test_transform_enumerations(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value


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
     # <documentation>
     #   <element id='0' name="anyName">
     #     <namespace/>
     #     <child id="0"/>
     #     <attribute name="anyName">
     #       <namespace/>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("count(/documentation/element)", 1),
         ("boolean(/documentation/element[@name = 'anyName'])", True),
         ("boolean(/documentation/element[@name = 'anyName']/child[1][@id = '0'])",
          True),
     ]
    ),
])
def test_transform_name_classes(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value


@pytest.mark.parametrize('xml,expected', [
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0"
                 xmlns:trans="http://docbook.org/ns/transclusion">
          <start>
            <ref name="test.define"/>
          </start>

          <define name="test.define">
            <element name="test">
              <attribute name="trans:test_attribute"/>
            </element>
          </define>
        </grammar>""",
     # <documentation>
     #   <element name="test" id="0">
     #     <namespace/>
     #     <attribute name="test_attribute">
     #       <namespace>http://docbook.org/ns/transclusion</namespace>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("boolean(/documentation/element[@name = 'test']/namespace/text())",
          False),
         ("/documentation/element[@name = 'test']/attribute/namespace/text()",
          ["http://docbook.org/ns/transclusion"]),
     ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <ref name="test.define"/>
          </start>

          <define name="test.define" xmlns:trans="http://docbook.org/ns/transclusion">
            <element name="test">
              <attribute name="trans:test_attribute"/>
            </element>
          </define>
        </grammar>""",
     # <documentation>
     #   <element name="test">
     #     <namespace/>
     #     <attribute name="test_attribute">
     #       <namespace>http://docbook.org/ns/transclusion</namespace>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("boolean(/documentation/element[@name = 'test']/namespace/text())",
          False),
         ("/documentation/element[@name = 'test']/attribute/namespace/text()",
          ["http://docbook.org/ns/transclusion"]),
     ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0"
                 xmlns:trans="http://docbook.org/ns/transclusion">
          <start>
            <ref name="test.define"/>
          </start>

          <define name="test.define">
            <element name="trans:test">
              <attribute name="test_attribute"/>
            </element>
          </define>
        </grammar>""",
     # <documentation>
     #   <element name="trans:test">
     #     <namespace>http://docbook.org/ns/transclusion</namespace>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("/documentation/element[@name = 'trans:test']/namespace/text()",
          ["http://docbook.org/ns/transclusion"]),
         ("/documentation/element[@name = 'trans:test']/attribute/namespace/text()",
          []),
     ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <ref name="test.define"/>
          </start>

          <define name="test.define">
            <element name="test" ns="http://www.example.com">
              <attribute name="test_attribute"/>
            </element>
          </define>
        </grammar>""",
     # <documentation>
     #   <element id='0' name="test">
     #     <namespace>http://www.example.com</namespace>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("/documentation/element[@name = 'test']/namespace/text()",
          ["http://www.example.com"]),
         ("/documentation/element[@name = 'test']/attribute/namespace/text()",
          []),
     ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <ref name="test.define"/>
          </start>

          <define name="test.define">
            <element name="test" ns="">
              <attribute name="test_attribute"/>
            </element>
          </define>
        </grammar>""",
     # <documentation>
     #   <element id='0' name="test">
     #     <namespace/>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("/documentation/element[@name = 'test']/namespace/text()",
          []),
         ("/documentation/element[@name = 'test']/attribute/namespace/text()",
          []),
     ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0">
          <start>
            <ref name="test.define"/>
          </start>

          <define name="test.define">
            <element name="test1" ns="http://www.example.com">
              <attribute name="test_attribute1"/>
              <element name="test2">
                <attribute name="test_attribute2"/>
              </element>
            </element>
          </define>
        </grammar>""",
     # <documentation>
     #   <element id='0' name="test1">
     #     <namespace>http://www.example.com</namespace>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     #   <element id='1' name="test2">
     #     <namespace>http://www.example.com</namespace>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("/documentation/element[@name = 'test1']/namespace/text()",
          ["http://www.example.com"]),
         ("/documentation/element[@name = 'test2']/namespace/text()",
          ["http://www.example.com"]),
         ("/documentation/element[@name = 'test1']/attribute/namespace/text()",
          []),
         ("/documentation/element[@name = 'test2']/attribute/namespace/text()",
          []),
    ]
    ),
    ("""<grammar xmlns="http://relaxng.org/ns/structure/1.0"
                 xmlns:trans="http://docbook.org/ns/transclusion">
          <start>
            <ref name="test.define"/>
          </start>

          <define name="test.define">
            <element name="trans:test" ns="http://www.example.com">
              <attribute name="test_attribute"/>
            </element>
          </define>
        </grammar>""",
     # <documentation>
     #   <element name="trans:test">
     #     <namespace>http://docbook.org/ns/transclusion</namespace>
     #     <attribute name="test_attribute">
     #       <namespace/>
     #       <type/>
     #       <use>required</use>
     #     </attribute>
     #   </element>
     # </documentation>
     [
         ("local-name(/*)", "documentation"),
         ("/documentation/element[@name = 'trans:test']/namespace/text()",
          ["http://docbook.org/ns/transclusion"]),
         ("/documentation/element[@name = 'trans:test']/attribute/namespace/text()",
          []),
     ]
    ),

])
def test_transform_namespaces(xml, expected):
    result = parse(io.StringIO(xml))
    assert isinstance(result, etree._ElementTree)
    for xpath, expected_value in expected:
        assert result.xpath(xpath) == expected_value
