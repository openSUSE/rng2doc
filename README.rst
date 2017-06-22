========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls|
        | |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/rng2doc/badge/?style=flat
    :target: https://readthedocs.org/projects/rng2doc
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/tomschr/rng2doc.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tomschr/rng2doc

.. |coveralls| image:: https://coveralls.io/repos/tomschr/rng2doc/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/tomschr/rng2doc

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/tomschr/rng2doc
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/tomschr/rng2doc/badges/gpa.svg
   :target: https://codeclimate.com/github/tomschr/rng2doc
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/rng2doc.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/rng2doc

.. |commits-since| image:: https://img.shields.io/github/commits-since/tomschr/rng2doc/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tomschr/rng2doc/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/rng2doc.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/rng2doc

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/rng2doc.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/rng2doc

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/rng2doc.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/rng2doc


.. end-badges

Converts a RELAX NG schema into documentation

* Free software: BSD license

Installation
============

::

    pip install rng2doc

Documentation
=============

https://rng2doc.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
