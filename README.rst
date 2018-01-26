=============
rng2doc 0.2.2
=============

Converts a RELAX NG schema into documentation (HTML).

* Free software: BSD license

Installation
============

Use your package manager or use the following instructions to install it
in a virtual environment::

    $ python3 -m venv .env
    $ source .env/bin/activate
    $ pip install -r requirements.txt
    $ pip install rng2doc


Development
===========

To run the all tests run::

    $ tox

To show the available target, run::

    $ tox -l

To run a code stylecheck (``flake8``), run::

    $ tox -e check

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
