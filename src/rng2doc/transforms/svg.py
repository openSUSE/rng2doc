"""Transform dictionary and functions for SVG
"""
# Third Party Libraries
import pydot

from ..common import (RNG_ANY_NAME,  # A_DOC,; RNG_DEFINE,
                      RNG_ATTRIBUTE,
                      RNG_CHOICE,
                      RNG_DATA,
                      RNG_DIV,
                      RNG_ELEMENT,
                      RNG_EMPTY,
                      RNG_EXCEPT,
                      RNG_GROUP,
                      RNG_INTERLEAVE,
                      RNG_LIST,
                      RNG_NS_NAME,
                      RNG_ONE_OR_MORE,
                      RNG_OPTIONAL,
                      RNG_PARAM,
                      RNG_TEXT,
                      RNG_VALUE,
                      RNG_ZERO_OR_MORE)


def transform_element_svg(node, **kwargs):
    """Transforms a RELAX NG element into a graphviz node.
    """
    name = node.get("name")
    if name is None:
        name = "anyName"
    name = '"' + name + '"'

    graphviz_attributes = {
        "label": name,
        "shape": "box",
        "style": '"rounded,filled"',
        "fillcolor": "#c0ffee"
    }

    root = kwargs.pop("root", False)
    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    if root:
        element = pydot.Node(name=identifier, **graphviz_attributes)
    else:
        element = pydot.Node(name=identifier, **graphviz_attributes)
    return element


def transform_attribute_svg(node, **kwargs):
    """Transforms a RELAX NG attribute into a graphviz node.
    """
    name = node.get("name")
    if name is None:
        name = "name class"
    name = '"' + name + '"'

    graphviz_attributes = {
        "label": name,
        "shape": "ellipse",
        "style": "filled",
        "fillcolor": "#fca9a9"
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_data_svg(node, **kwargs):
    """Transforms a RELAX NG data into a graphviz node.
    """
    name = node.get("type")
    name = '"' + name + '"'

    graphviz_attributes = {
        "label": name,
        "shape": "ellipse",
        "style": "filled",
        "fillcolor": "#a9bdfc",
    }
    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_value_svg(node, **kwargs):
    """Transforms a RELAX NG value into a graphviz node.
    """
    if node.text is None:
        name = node.attrib["datatypeLibrary"]
    else:
        name = node.text
    name = '"' + name + '"'

    graphviz_attributes = {
        "label": name,
        "shape": "ellipse",
        "style": "filled",
        "fillcolor": "#a2a4aa",
    }
    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_param_svg(node, **kwargs):
    """Transforms a RELAX NG param into a graphviz node.
    """
    name = node.get("name")
    name = '"' + name + '"'

    graphviz_attributes = {
        "label": name,
        "shape": "ellipse",
        "style": "filled",
        "fillcolor": "#f9d368",
    }
    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_ns_name_svg(node, **kwargs):
    """Transforms a RELAX NG nsName into a graphviz node.
    """
    namespace = node.get("ns")
    if namespace is None:
        namespace = "No Namespace"
    name = namespace
    name = '"' + name + '"'

    graphviz_attributes = {
        "label": name,
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_interleave_svg(node, **kwargs):
    """Transforms a RELAX NG interleave into a graphviz node.
    """
    graphviz_attributes = {
        "label": "&",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_zero_or_more_svg(node, **kwargs):
    """Transforms a RELAX NG zeroOrMore into a graphviz node.
    """
    graphviz_attributes = {
        "label": "*",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_one_or_more_svg(node, **kwargs):
    """Transforms a RELAX NG oneOrMore into a graphviz node.
    """
    graphviz_attributes = {
        "label": "+",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_optional_svg(node, **kwargs):
    """Transforms a RELAX NG optional into a graphviz node.
    """
    graphviz_attributes = {
        "label": "?",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_choice_svg(node, **kwargs):
    """Transforms a RELAX NG choice into a graphviz node.
    """
    graphviz_attributes = {
        "label": "|",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_except_svg(node, **kwargs):
    """Transforms a RELAX NG except into a graphviz node.
    """
    graphviz_attributes = {
        "label": "-",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_group_svg(node, **kwargs):
    """Transforms a RELAX NG group into a graphviz node.
    """
    graphviz_attributes = {
        "label": "group",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_list_svg(node, **kwargs):
    """Transforms a RELAX NG list into a graphviz node.
    """
    graphviz_attributes = {
        "label": "list",
        "shape": "circle",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_text_svg(node, **kwargs):
    """Transforms a RELAX NG text into a graphviz node.
    """
    graphviz_attributes = {
        "label": "text",
        "shape": "rect",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_empty_svg(node, **kwargs):
    """Transforms a RELAX NG empty into a graphviz node.
    """
    graphviz_attributes = {
        "label": "empty",
        "shape": "rect",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_any_name_svg(node, **kwargs):
    """Transforms a RELAX NG anyName into a graphviz node.
    """
    graphviz_attributes = {
        "label": "anyName",
        "shape": "rect",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_div_svg(node, **kwargs):
    """Transforms a RELAX NG div into a graphviz node.
    """
    graphviz_attributes = {
        "label": "div",
        "shape": "rect",
    }

    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def transform_a_doc_svg(node, **kwargs):
    """Transforms a documentation string into a graphviz node.
    """
    name = node.text
    name = '"' + name + '"'

    graphviz_attributes = {
        "label": name,
    }
    index = kwargs.pop("index", False)
    identifier = "node{}".format(index)

    return pydot.Node(name=identifier, **graphviz_attributes)


def append_method_svg(node, parent, **kwargs):
    """The append method to form a graph via pydot.
    """
    root = kwargs.pop("root", False)
    graph = kwargs.pop("graph", None)
    graph.add_node(node)
    if not root:
        graph.add_edge(pydot.Edge(parent, node))


SVG = {
    # RNG_DEFINE: unknown_tag,
    RNG_ELEMENT: transform_element_svg,
    RNG_EMPTY: transform_empty_svg,
    RNG_ATTRIBUTE: transform_attribute_svg,
    RNG_ZERO_OR_MORE: transform_zero_or_more_svg,
    RNG_ONE_OR_MORE: transform_one_or_more_svg,
    RNG_LIST: transform_list_svg,
    RNG_GROUP: transform_group_svg,
    RNG_OPTIONAL: transform_optional_svg,
    RNG_INTERLEAVE: transform_interleave_svg,
    RNG_CHOICE: transform_choice_svg,
    RNG_DATA: transform_data_svg,
    RNG_TEXT: transform_text_svg,
    RNG_PARAM: transform_param_svg,
    RNG_VALUE: transform_value_svg,
    RNG_ANY_NAME: transform_any_name_svg,
    RNG_NS_NAME: transform_ns_name_svg,
    RNG_EXCEPT: transform_except_svg,
    RNG_DIV: transform_div_svg,
    # A_DOC: transform_a_doc_svg,
    "append": append_method_svg,
}
