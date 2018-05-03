"""Parsing RNG file and creating intermediate structure

"""

# Standard Library
import logging

# Third Party Libraries
from lxml import etree

# Local imports
from .common import (A_DOC,
                     NSMAP,
                     RNG_ATTRIBUTE,
                     RNG_CHOICE,
                     RNG_DATA,
                     RNG_DEFINE,
                     RNG_ELEMENT,
                     RNG_OPTIONAL,
                     RNG_PARAM,
                     RNG_REF,
                     RNG_TEXT,
                     RNG_VALUE)
from .exceptions import NoMatchinRootException

log = logging.getLogger(__name__)


#  gh://openSUSE/xmldiffng:xmldiffng/contrib/parse-rng.py


def strip_newlines(string):
    """Removes all newline characters from a string

     :param string: Some string
     :type str: str
     :return: The string without newlines
     :rtype: str
    """
    return string.replace("\n", "").replace("\r", "").strip()


def transform_child(element, output, tree):
    """Transforms a "rlxng element" element which is child of another "rlxng element"

     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed attributes
     :rtype: etree.Element
    """
    uuid = element.get("id")
    etree.SubElement(output, "child", id=uuid)
    return output


def transform_data_type(element, output, tree):
    """Transforms a "rlxng data" element

     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed attributes
     :rtype: etree.Element
    """
    attribute_type = etree.SubElement(output, "type")
    description_type = etree.SubElement(attribute_type, "description")
    param = etree.SubElement(attribute_type, "param")
    data_type = descendants(RNG_DATA, element, None, tree)
    if data_type:
        attribute_type.attrib["name"] = data_type
        description = find_doc_string(element.find(RNG_DATA.text))
        if description:
            description_type.text = description
        _param = descendants(RNG_PARAM, element, None, tree)
        if _param:
            param.attrib["name"], param.text = _param
        return output
    data_type = descendants(RNG_TEXT, element, None, tree)
    if data_type:
        attribute_type.attrib["name"] = data_type
        return output
    values = descendants(RNG_CHOICE, element, None, tree)
    if values:
        attribute_type.attrib["name"] = "enum"
        for value, _description in values:
            value_tag = etree.SubElement(attribute_type, "value")
            description_value = etree.SubElement(value_tag, "description")
            value_tag.attrib["name"] = value
            if _description:
                description_value.text = _description
        return output
    return output


def find_namespace(element):
    name = element.get("name")
    if name and len(name.split(":")) > 1:
        prefix = name.split(":")[0]
        if prefix in element.nsmap:
            return element.nsmap[prefix]
        elif prefix == "xml":
            return "http://www.w3.org/XML/1998/namespace"
    namespace = element.get("ns")
    if namespace:
        return namespace
    if element.tag == RNG_ATTRIBUTE.text:
        return None
    if element.tag == RNG_ELEMENT.text:
        namespace = element.xpath("ancestor::node()[@ns][1]")
    if namespace:
        return namespace[0].get("ns")
    return None


def transform_attribute(element, output, tree):
    """Transforms a "rlxng attribute" element

     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed attributes
     :rtype: etree.Element
    """
    attribute = etree.SubElement(output, "attribute")
    etree.SubElement(attribute, "name").text = element.get("name")
    namespace = etree.SubElement(attribute, "namespace")
    if find_namespace(element):
        namespace.text = find_namespace(element)
    description = etree.SubElement(attribute, "description")
    doc_string = find_doc_string(element)
    if doc_string:
        description.text = doc_string
    attribute = transform_data_type(element, attribute, tree)

    optional = ascendants(RNG_OPTIONAL, element, RNG_ATTRIBUTE, None, tree)
    if optional:
        etree.SubElement(attribute, "use").text = "optional"
    else:
        etree.SubElement(attribute, "use").text = "required"
    return output


def ascendants(qname, element, end, output, tree):
    """Finds all ascendants of a specific qname and follows
       the references to its defines.

     :param qname: Specifies the tag and the namespaces
     :type qname: etree.QName
     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The output + all ascendants which match
     :rtype: etree.Element
    """
    parents = []
    parents.append(element.getparent())
    for parent in parents:
        if parent is None:
            return None
        if parent.tag == end.text:
            continue
        if parent.tag == qname.text:
            if parent.tag == RNG_OPTIONAL.text:
                return True
            if parent.tag == RNG_DEFINE.text:
                return parent.get("name")

        if parent.tag == RNG_DEFINE.text:
            ref_name = parent.get("name")
            next_parents = ".//{}[@name='{}']".format(RNG_REF.text, ref_name)
            parents += tree.findall(next_parents)
        else:
            parents.append(parent.getparent())
    return output


def descendants(qname, element, output, tree):
    """Finds all descendants of a specific qname and follows
       the references to its defines.

     :param qname: Specifies the tag and the namespaces
     :type qname: etree.QName
     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The output + all descendants which match
     :rtype: etree.Element
    """
    children = element.getchildren()
    for child in children:

        if child.tag == RNG_ELEMENT.text:
            if child.tag == qname.text:
                output = transform_child(child, output, tree)
            continue

        if child.tag == qname.text:
            if qname.text == RNG_ATTRIBUTE.text:
                output = transform_attribute(child, output, tree)
            if qname.text == RNG_DATA.text:
                return child.get("type")
            if qname.text == RNG_TEXT.text:
                return "text"
            if qname.text == RNG_CHOICE.text:
                values = []
                values = descendants(RNG_VALUE, child, values, tree)
                return values
            if qname.text == RNG_PARAM.text:
                return (child.get("name"), child.text)
            if qname.text == RNG_VALUE.text:
                description = ""
                for sibling in child.itersiblings():
                    if sibling.tag == A_DOC.text:
                        description = sibling.text
                        break
                output.append(
                    (child.text, description)
                )

        if child.tag == RNG_REF.text:
            anchor_name = child.get("name")
            anchors = ".//{}[@name='{}']".format(RNG_DEFINE.text, anchor_name)
            children += tree.findall(anchors)

        children += child.getchildren()
    return output


def find_doc_string(element):
    """Finds documentation string of an specific element

     :param element: A rlxng element
     :type element: etree.Element
     :return: The documentation string of the given element or an empty string.
     :rtype: str
    """
    doc_string = None
    if element is not None:
        doc_string = element.find("{}".format(A_DOC))
    if doc_string is not None:
        return strip_newlines(doc_string.text)
    return ""


def find_children(element, output, tree):
    """Finds all child elements of specific element

     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed attributes
     :rtype: etree.Element
    """
    return descendants(RNG_ELEMENT, element, output, tree)


def find_attributes(element, output, tree):
    """Finds all attribute elements of specific element

     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed attributes
     :rtype: etree.Element
    """
    return descendants(RNG_ATTRIBUTE, element, output, tree)


def transform_element(element, tree):
    """Transforms a "rlxng element" element

     :param element: A rlxng element
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed element
     :rtype: etree.Element
    """
    name = element.get("name")
    uuid = element.get("id")
    if name is None:
        name = ascendants(RNG_DEFINE, element, RNG_ELEMENT, None, tree)
    transformed_element = etree.Element("element", name=name, id=uuid)
    namespace = etree.SubElement(transformed_element, "namespace")
    if find_namespace(element):
        namespace.text = find_namespace(element)
    description = etree.SubElement(transformed_element, "description")
    doc_string = find_doc_string(element)
    if doc_string:
        description.text = find_doc_string(element)
    transformed_element = find_children(element, transformed_element, tree)
    transformed_element = find_attributes(element, transformed_element, tree)
    return transformed_element


def transform(rngfilename, elementdef=None):
    """Read RNG file and transform it to the XML-Documentation format

     :param rngfilename: path to the RNG file (in XML format)
     :type rngfilename: str
     :return: The ElementTree of the new XML document
     :rtype: etree.ElementTree
    """
    xmlparser = None

    rngtree = etree.parse(rngfilename, xmlparser)

    root = etree.QName(rngtree.getroot())
    if root.namespace != NSMAP['rng']:
        raise NoMatchinRootException("Wrong namespace in root element %s. "
                                     "Expected namespace from RELAX NG" % root.text)

    documentation = etree.Element("documentation")
    elements = rngtree.xpath("//rng:element", namespaces=NSMAP)
    index = 0
    for element in elements:
        uuid = "{}".format(index)
        element.attrib["id"] = uuid
        index += 1
    for element in elements:
        documentation.append(transform_element(element, rngtree))
    return etree.ElementTree(documentation)


def process(args):
    """Process RELAX NG file

    :param args: result dictionary from :class:`docopt.docopt`
    :return: The ElementTree of new XML document
    :rtype: etree.ElementTree
    """
    rngfile = args['RNGFILE']
    log.info("Process RNG file %r...", rngfile)
    return transform(rngfile)
