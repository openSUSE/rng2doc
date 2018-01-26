=============
rng2doc 0.2.1
=============

Converts a RELAX NG schema into documentation (HTML).

* Free software: BSD license

Installation
============

::

    pip install rng2doc


Development
===========

To run the all tests run::

    $ tox

To show the available target, run::

    $ tox -l

To run a code stylecheck (``flake8``), run::

    $ tox check

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
