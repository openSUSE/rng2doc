"""Parsing RNG file and creating intermediate structure

"""

# Standard Library
import logging

# Third Party Libraries
import graphviz as gv
from lxml import etree

# Local imports
from .common import (A_DOC,
                     NSMAP,
                     # RNG_GRAMMAR,
                     # RNG_START,
                     # RNG_INCLUDE,
                     RNG_DEFINE,
                     RNG_REF,
                     # RNG_EXTERNAL_REF,
                     RNG_ELEMENT,
                     RNG_ATTRIBUTE,
                     RNG_ZERO_OR_MORE,
                     RNG_ONE_OR_MORE,
                     RNG_LIST,
                     RNG_GROUP,
                     RNG_OPTIONAL,
                     RNG_INTERLEAVE,
                     RNG_CHOICE,
                     RNG_DATA,
                     RNG_TEXT,
                     RNG_PARAM,
                     RNG_VALUE,
                     RNG_ANY_NAME,
                     RNG_NS_NAME,
                     RNG_EXCEPT,
                     RNG_DIV,
                     RNG_EMPTY,
                     DB_PARA,
                     SCH_PATTERN,
                     SCH_PARAM,
                     SCH_RULE,
)
from .exceptions import NoMatchinRootException

log = logging.getLogger(__name__)


#  gh://openSUSE/xmldiffng:xmldiffng/contrib/parse-rng.py

class RngIterator:
    def __init__(self, qname, node, defines):
        self.node = None
        self.next_node = node
        self.defines = defines
        self.qname = qname
        self.children = node.getchildren()
        self.children.reverse()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.node = self.next_node
            self.next_node = self.children.pop()
            if self.next_node.tag == RNG_ELEMENT.text:
                self.node = self.next_node
                if self.children:
                    self.next_node = self.children.pop()
                else:
                    return self.node
            if self.qname.text == self.next_node.tag:
                if self.children:
                    self.next_node = self.children.pop()
                else:
                    return self.node

            if self.next_node.tag == RNG_REF.text:
                self.children += self.defines[self.next_node.get("name")]

            next_children = self.next_node.getchildren()
            next_children.reverse()
            self.children += next_children
            return self.node
        except IndexError:
            raise StopIteration


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


def transform_data(element, output, tree):
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
    description_type = etree.SubElement(output, "description")
    param = etree.SubElement(output, "param")
    description = find_doc_string(element.find(RNG_DATA.text))
    if description:
        description_type.text = description
    param_tuple = descendants(RNG_PARAM, element, None, tree)
    if param_tuple:
        param.attrib["name"], param.text = param_tuple
    return output


def transform_text(element, output, tree):
    """Transforms a "rlxng text" element

     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed attributes
     :rtype: etree.Element
    """
    etree.SubElement(output, "description")
    param = etree.SubElement(output, "param")
    param_tuple = descendants(RNG_PARAM, element, None, tree)
    if param_tuple:
        param.attrib["name"], param.text = param_tuple
    return output


def transform_enum(values, output, tree):
    """Transforms a "rlxng enum"

     :param element: A rlxng element
     :type element: etree.Element
     :param element: The transformed output so far
     :type element: etree.Element
     :param tree: The whole tree of the original file
     :type tree: etree.ElementTree
     :return: The transformed attributes
     :rtype: etree.Element
    """
    etree.SubElement(output, "description")
    etree.SubElement(output, "param")
    for value, description_text in values:
        value_tag = etree.SubElement(output, "value")
        description = etree.SubElement(value_tag, "description")
        value_tag.attrib["name"] = value
        if description_text:
            description.text = description_text
    return output


def transform_data_type(element, output, tree):
    """Transforms the datatype of the attribute

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

    data_type = descendants(RNG_DATA, element, None, tree)
    if data_type:
        attribute_type.attrib["name"] = data_type
        attribute_type = transform_data(element, attribute_type, tree)
        return output

    data_type = descendants(RNG_TEXT, element, None, tree)
    if data_type:
        attribute_type.attrib["name"] = data_type
        attribute_type = transform_text(element, attribute_type, tree)
        return output

    values = descendants(RNG_CHOICE, element, None, tree)
    if values:
        attribute_type.attrib["name"] = "enum"
        attribute_type = transform_enum(values, attribute_type, tree)
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


def t_node(index, node):
    identifier = "node{}".format(index)
    name = node.tag
    styles = {
        "width": "0.6",
    }

    if node.tag == RNG_ELEMENT.text:
        identifier = "{}{}".format(
            node.get("name"),
            node.get("id"))
        name = node.get("name")
        if name is None:
            name = "name class"
        styles["shape"] = "box"
        styles["style"] = "rounded,filled"
        styles["fillcolor"] = "#c0ffee"

    if node.tag == RNG_ATTRIBUTE.text:
        name = node.get("name")
        if name is None:
            name = "name class"
        styles["shape"] = "ellipse"
        styles["style"] = "filled"
        styles["fillcolor"] = "#fca9a9"

    if node.tag == RNG_DEFINE.text:
        name = node.get("name")

    if node.tag == RNG_DATA.text:
        name = node.get("type")
        styles["shape"] = "ellipse"
        styles["style"] = "filled"
        styles["fillcolor"] = "#a9bdfc"

    if node.tag == RNG_VALUE.text:
        name = node.text
        styles["shape"] = "ellipse"
        styles["style"] = "filled"
        styles["fillcolor"] = "#a2a4aa"

    if node.tag == RNG_PARAM.text:
        param_name = node.get("name")
        param_value = node.text
        # name = "{} = {}".format(param_name, param_value)
        name = param_name
        styles["shape"] = "ellipse"
        styles["style"] = "filled"
        styles["fillcolor"] = "#f9d368"

    if node.tag == RNG_NS_NAME.text:
        namespace = node.get("ns")
        if namespace is None:
            namespace = "No Namespace"
        name = namespace
        styles["shape"] = "ellipse"

    if node.tag == RNG_INTERLEAVE.text:
        name = "&"
        styles["shape"] = "circle"

    if node.tag == RNG_ZERO_OR_MORE.text:
        name = "*"
        styles["shape"] = "circle"

    if node.tag == RNG_ONE_OR_MORE.text:
        name = "+"
        styles["shape"] = "circle"

    if node.tag == RNG_OPTIONAL.text:
        name = "?"
        styles["shape"] = "circle"

    if node.tag == RNG_CHOICE.text:
        name = "|"
        styles["shape"] = "circle"

    if node.tag == RNG_EXCEPT.text:
        name = "-"
        styles["shape"] = "circle"

    if node.tag == RNG_GROUP.text:
        name = "group"
        styles["shape"] = "circle"

    if node.tag == RNG_LIST.text:
        name = "list"
        styles["shape"] = "circle"

    if node.tag == RNG_TEXT.text:
        name = "Text"
        styles["shape"] = "rect"

    if node.tag == RNG_EMPTY.text:
        name = "Empty"
        styles["shape"] = "rect"

    if node.tag == RNG_ANY_NAME.text:
        name = "anyName"
        styles["shape"] = "rect"

    if node.tag == RNG_DIV.text:
        name = "div"
        styles["shape"] = "rect"

    if node.tag == A_DOC.text:
        name = node.text

    return identifier, name, styles


# Maybe it's not necessary to handover the graph every time
# It should be possible to create Nodes and Edges without the
# graph object via pydot.
def visualize(node, graph, simple=True, parent=None, counter=0):
    # The namespace of the nodes is missing and
    # Elements from foreign namespaces are just shown in
    # the clark notation.

    # Handle the root element of the tree
    if parent is None:
        parent, root, styles = t_node(counter, node)
        graph.node(parent, root, styles)
        counter += 1

    children = node.getchildren()
    if not children:
        return counter, graph

    for child in children:

        # FIXME
        # The function t_node keeps the transformation seperate.
        # But it makes it is still quite difficult to add new
        # Transformation functions. I need to improve this
        identifier, name, styles = t_node(counter, child)
        
        # The simple mode will add only the children of the
        # type RNG_ELEMENT and RNG_ATTRIBUTE to the graph
        if(
             simple and
             child.tag != RNG_ELEMENT.text and
             child.tag != RNG_ATTRIBUTE.text and
             child.tag != RNG_REF
          ):
            counter += 1
            counter, graph = visualize(
                child, graph, parent=parent, counter=counter)     
        elif(
            child.tag == RNG_DEFINE.text or 
            child.tag == A_DOC.text or
            child.tag == DB_PARA.text or
            child.tag == SCH_PARAM.text or
            child.tag == SCH_PATTERN.text or
            child.tag == SCH_RULE
          ):
            # FIXME
            # Skip the define and the doc annotations node.
            # Skipping means to set the parent node as new parent node not
            # the current node.
            #
            # I need some kind of tooltip design for the annotation node. The
            # doc string now will enlarge the graph enormously.
            #
            # It's necessary to rearrange the graph into Clusters
            # I need to implement it like this:
            # http://robertyu.com/wikiperdido/Pydot%20Clusters
            counter += 1
            counter, graph = visualize(
                child, graph, parent=parent, counter=counter)
        elif child.tag == RNG_REF.text:
            xpath = "//rng:define[@name = '{}']".format(child.get("name"))
            define = node.xpath(xpath, namespaces=NSMAP).pop()
            counter += 1
            counter, graph = visualize(
                define, graph, parent=parent, counter=counter)
        else:
            # Iterate through all the elements in the tree and transform the
            # tag to a visual graph node.
            graph.node(identifier, name, styles)
            graph.edge(parent, identifier)

            # The iteration will stop if some new Element will be found in that
            # branch.
            if child.tag == RNG_ELEMENT.text:
                continue

            counter += 1
            # Transform the children of the current node, too.
            # That the identifier of the current node as parent
            # and the child as current node.
            counter, graph = visualize(
                child, graph, parent=identifier, counter=counter)
    return counter, graph


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
    graph = gv.Graph(format="svg")
    graph.graph_attr["rankdir"] = "LR"
    _, graph = visualize(element, graph)
    svg = etree.fromstring(graph.pipe())
    transformed_element.append(svg)
    return transformed_element


def populate_references_map(rngtree):
    ref_map = {}
    for node in rngtree.iter():
        if node.tag == RNG_DEFINE.text:
            ref_map[node.get("name")] = node
    return ref_map


def add_unique_index(elements):
    index = 0
    for element in elements:
        uuid = "{}".format(index)
        element.attrib["id"] = uuid
        index += 1
    return elements


def transform(rngfilename):
    """Read RNG file and transform it to the XML-Documentation format

     :param rngfilename: path to the RNG file (in XML format)
     :type rngfilename: str
     :return: The ElementTree of the new XML document
     :rtype: etree.ElementTree
    """
    # Remove all blank lines, which makes the output later much more beautiful
    # :-)
    xmlparser = etree.XMLParser(remove_blank_text=True, remove_comments=True)

    rngtree = etree.parse(rngfilename, xmlparser)

    root = etree.QName(rngtree.getroot())
    if root.namespace != NSMAP['rng']:
        raise NoMatchinRootException("Wrong namespace in root element %s. "
                                     "Expected namespace from RELAX NG" % root.text)

#   Generates a define map which make it easier to find the define for on ref.
#   Maybe this is too memory expensive and a xpath expression like
#   xpath(//define[@name = $ref]) is faster and more efficient.
#    refs = rngtree.xpath("//rng:ref", namespaces=NSMAP)
#    define_map = populate_references_map(rngtree)

#   It's not possible to resolve all links because of the recursive ref feature
#   of RELAX NG.
#      for ref in refs:
#          try:
#              parent = ref.getparent()
#              parent.insert(
#                  parent.index(ref)+1,
#                  define_map[ref.get("name")]
#              )
#              parent.remove(ref)
#          except:
#              print(ref.get("name"))

    elements = rngtree.xpath("//rng:element", namespaces=NSMAP)
#   Adds a unique id for every element in the tree
    elements = add_unique_index(elements)


#   The root element of my output format
    documentation = etree.Element("documentation")

#   Collect information about every element in the schema and transform it
#   to the output format.
    for element in elements:
        documentation.append(
            transform_element(element, rngtree))
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
