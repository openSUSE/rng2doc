:orphan:

rng2doc Manual Page
===================

Synopsis
--------

.. _invocation:

.. sourcecode:: bash

     $ rng2doc [-h | --help]
     $ rng2doc [-v ...] [options] RNGFILE


Description
-----------

:program:`rng2doc` generates "API documentation" from a RELAX NG schema.
It analyzes the RNG schema, collects all elements, attributes, and their
documentation strings and creates an output format. You can select if you
want XML (an internal, cleaned up representation of the RNG tree) or HTML.

The XML format can be used for further processing by XSLT stylesheets or
other tools.

When you create HTML, each element has its own HTML page. Each HTML page
contains:

* The element description
* The element's namespace
* A (SVG) graph



Options
-------

.. program:: rng2doc

.. option:: -h, --help, --version

   Display usage summary or script version.

.. option:: -v, --verbose

   Increase verbosity (can be repeated).

.. option:: --output=<OUTFILE>

   Optional file where results are written to

.. option:: --output-format=<FORMAT>, -f <FORMAT>

   Specifies the format of the output. (xml, html) [default: xml]

.. option:: RNGFILE

   Path to RELAX NG file (file extension .rng)


Examples
--------

.. TODO: The following items needs a bit more care:

* Create a XML file from :file:`foo.rng` and print its output to stdout::

    $ rng2doc foo.rng

* Creates a XML file from :file:`foo.rng` and save the output to
  :file:`/tmp/foo.xml`::

    $ rng2doc --output /tmp/foo.xml foo.rng

* Create HTML output from :file:`foo.rng`::

    $ rng2doc --output-format=html foo.rng


See also
--------

* RELAX NG specification: http://relax.org


Authors
-------

* Jürgen Löhel for SUSE Linux GmbH
* Thomas Schraitle, mentoring
