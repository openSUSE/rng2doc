"""Transform dictionary and functions for XML
"""
# Third Party Libraries
from lxml import etree

# Local imports
from ..common import (A_DOC,
                      NSMAP,
                      RNG_ATTRIBUTE,
                      RNG_CHOICE,
                      RNG_DATA,
                      RNG_ELEMENT,
                      RNG_OPTIONAL,
                      RNG_PARAM,
                      RNG_TEXT,
                      RNG_VALUE)


def find_namespace(node):
    """Finds the namespace for a node.
    """
    name = node.get("name")
    if name and len(name.split(":")) > 1:
        prefix = name.split(":")[0]
        if prefix in node.nsmap:
            return node.nsmap[prefix]
        elif prefix == "xml":
            return NSMAP['xml']
    namespace = node.get("ns")
    if namespace:
        return namespace
    if node.tag == RNG_ATTRIBUTE.text:
        return None
    if node.tag == RNG_ELEMENT.text:
        namespace = node.xpath("ancestor::node()[@ns][1]")
    if namespace:
        return namespace[0].get("ns")
    return None


def transform_element(node, **kwargs):
    """Transforms a RELAX NG element into a new XML structure
    """
    root = kwargs.pop("root", False)
    uuid = node.get("id")
    name = node.get("name")
    if name is None:
        name = "anyName"
    if root:
        namespace = find_namespace(node)
        element = etree.Element("element", name=name, id=uuid)
        element_namespace = etree.SubElement(element, "namespace")
        if namespace:
            element_namespace.text = namespace
    else:
        element = etree.Element("child", id=uuid)
    return element


def transform_attribute(node, **kwargs):
    """Transforms a RELAX NG attribute into a new XML structure
    """
    optional = kwargs.pop("optional", False)
    name = node.get("name")
    if name is None:
        name = "anyName"
    attribute = etree.Element("attribute", name=name)
    attribute_namespace = etree.SubElement(
        attribute, "namespace")
    namespace = find_namespace(node)
    attribute_use = etree.SubElement(attribute, "use")
    if optional:
        attribute_use.text = "optional"
    else:
        attribute_use.text = "required"
    if namespace:
        attribute_namespace.text = namespace
    return attribute


def transform_description(node, **kwargs):
    """Transforms a RELAX NG documentation string into a new XML structure
    """
    description = etree.Element("description")
    description.text = node.text
    return description


def transform_text(node, **kwargs):
    """Transforms a RELAX NG text into a new XML structure
    """
    data_type = etree.Element("type")
    data_type.attrib["name"] = "text"
    return data_type


def transform_data(node, **kwargs):
    """Transforms a RELAX NG data into a new XML structure
    """
    data_type = etree.Element("type")
    data_type.attrib["name"] = node.get("type")
    return data_type


def transform_param(node, **kwargs):
    """Transforms a RELAX NG param into a new XML structure
    """
    param = etree.Element("param")
    name = node.get("name")
    value = node.text
    param.attrib["name"] = name
    param.text = value
    return param


def transform_choice(node, **kwargs):
    """Sets the choice flag.
    """
    return "choice"


def transform_value(node, **kwargs):
    """Transforms a RELAX NG value into a new XML structure
    """
    value = etree.Element("value")
    if node.text is None:
        value.attrib["name"] = node.attrib["datatypeLibrary"]
    else:
        value.attrib["name"] = node.text
    if node.getnext() is not None and node.getnext().tag == A_DOC.text:
        description = etree.SubElement(value, "description")
        description.text = node.getnext().text
    return value


def transform_optional(node, **kwargs):
    """Sets the optional flag.
    """
    return "optional"


def append_method_xml(node, transformation, **kwargs):
    """The append method for lxml
    """
    transformation.append(node)


XML = {
    RNG_ELEMENT: transform_element,
    RNG_ATTRIBUTE: transform_attribute,
    RNG_OPTIONAL: transform_optional,
    RNG_CHOICE: transform_choice,
    RNG_DATA: transform_data,
    RNG_TEXT: transform_text,
    RNG_PARAM: transform_param,
    RNG_VALUE: transform_value,
    A_DOC: transform_description,
    "append": append_method_xml,
}
