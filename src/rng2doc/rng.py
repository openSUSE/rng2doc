"""Parsing, Transforming, Visualizing the RELAX NG structure.
"""

# Standard Library
from pkg_resources import resource_filename

# Third Party Libraries
import pydot
from lxml import etree

# Local imports
from .common import NSMAP, RNG_ELEMENT, RNG_REF, RNG_VALUE
from .log import logger
from .transforms.svg import SVG
from .transforms.xml import XML


def transform(node, output, **kwargs):
    """General transformation of RELAX NG

    :param node: The node which should be transformed
    :type node: etree.Element
    :param output: The output of the transformation.
    :param kwargs: Options for the transformation
    :return: The same list of etree.Elements with a unique index.
    :rtype: A list of etree.Element
    """
    parent = kwargs.pop("parent", None)
    choice = kwargs.pop("choice", None)
    optional = kwargs.pop("optional", False)
    template = kwargs.pop("template", XML)
    index = kwargs.pop("index", 0)
    append = template.get("append")

    if parent is None:
        if node.tag != RNG_ELEMENT.text:
            return output
        transform_func = template.get(node.tag)
        transformed_node = transform_func(node, root=True, index=index)
        append(transformed_node, output, graph=output, root=True)
        parent = transformed_node

    children = node.getchildren()

    for child in children:
        transform_func = template.get(child.tag)
        if child.tag == RNG_REF.text:
            xpath = "//rng:define[@name = '{}']".format(child.get("name"))
            define = node.xpath(xpath, namespaces=NSMAP).pop()
            output, index = transform(
                define, output,
                index=index,
                parent=parent, optional=optional, choice=choice,
                template=template)
        if child.tag == RNG_VALUE.text and choice is not None and template == XML:
            transformed_node = transform_func(child)
            append(transformed_node, choice)
            append(choice, parent)
            output, index = transform(
                child, output,
                index=index,
                parent=transformed_node, optional=optional, choice=None,
                template=template)
        elif transform_func is None:
            output, index = transform(
                child, output,
                index=index,
                parent=parent, optional=optional, choice=choice,
                template=template)
        else:
            index += 1
            transformed_node = transform_func(child, optional=optional, index=index)
            if transformed_node == "optional" and template == XML:
                optional = True
                transformed_node = parent
            elif transformed_node == "choice" and template == XML:
                choice = etree.Element("type")
                choice.attrib["name"] = "enum"
                transformed_node = parent
            else:
                append(transformed_node, parent, graph=output)
            if child.tag == RNG_ELEMENT.text:
                continue

            output, index = transform(
                child, output,
                index=index,
                parent=transformed_node, optional=optional, choice=choice,
                template=template)

        if optional:
            optional = None

    return output, index


def add_unique_index(elements):
    """Adds a unique index to all RELAX NG elements.

    :param elements: A list of RELAX NG elements.
    :type elements: A list of etree.Element
    :return: The same list of etree.Elements with a unique index.
    :rtype: A list of etree.Element
    """
    for index, element in enumerate(elements):
        uuid = "{}".format(index)
        element.attrib["id"] = uuid
    return elements


def parse(rngfile):
    """Read RNG file and transform it to the XML-Documentation format

     :param rngfilename: path to the RNG file (in XML format)
     :type rngfilename: str
     :return: The ElementTree of the new XML document
     :rtype: etree.ElementTree
    """
    logger.info("Process RNG file %r...", rngfile)

    # Remove all blank lines, which makes the output later much more beautiful.
    xmlparser = etree.XMLParser(remove_blank_text=True, remove_comments=True)

    relaxng_schema = etree.parse(resource_filename(__package__, "schemas/relaxng.rng"))
    relaxng = etree.RelaxNG(relaxng_schema)
    rngtree = etree.parse(rngfile, xmlparser)
    if not relaxng.validate(rngtree):
        raise RuntimeError("The input file is not a valid RELAX NG document.")

    elements = rngtree.xpath("//rng:element", namespaces=NSMAP)
    elements = add_unique_index(elements)

    documentation = etree.Element("documentation")

    for element in elements:
        name = element.get("name")
        if name is None:
            name = "anyName"
        element_id = element.attrib["id"]
        documentation, _ = transform(element, documentation, template=XML)

        name = '"' + name + '"'
        graph = pydot.Dot(graph_name=name, rankdir="LR", format="svg")
        graph, _ = transform(element, graph, template=SVG)
        svg = etree.fromstring(graph.create_svg())
        svg.attrib.pop("width")
        svg.attrib.pop("height")

        # Inject the SVG
        xpath = "//element[@id={}]".format(element_id)
        documentation.xpath(xpath).pop().append(svg)
    return etree.ElementTree(documentation)
