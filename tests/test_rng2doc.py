# Standard Library
import logging
import os
from unittest.mock import patch

# Third Party Libraries
import pytest

# My Stuff
import rng2doc
from rng2doc.cli import main

# log = logging.getLogger(rng2doc.__package__)


def test_main():
    assert main([]) == 10


def test_main_with_version(capsys):
    """Checks for correct version"""
    with pytest.raises(SystemExit):
        main([rng2doc.__package__, "--version"])
    out, _ = capsys.readouterr()
    assert out == "{} {}\n".format(rng2doc.__package__, rng2doc.__version__)


def test_main_with_capsys():
    """Checks, if __main__.py can be executed"""
    with pytest.raises(SystemExit):
        path = os.path.dirname(os.path.realpath(__file__)) +\
               "/../src/{}/__main__.py".format(rng2doc.__package__)
        exec(compile(open(path).read(), path, "exec"), {}, {"__name__": "__main__"})


@patch('rng2doc.cli.os.path.exists')
def test_main_notfound_rng(mock_exists):
    mock_exists.return_value = False
    result = main([rng2doc.__package__, "fake.rng"])
    assert result != 0


@patch('rng2doc.cli.os.path.exists')
def test_main_with_KeyboardInterrupt(mock_exists):
    mock_exists.side_effect = KeyboardInterrupt()
    result = main([rng2doc.__package__, "fake.rng"])
    assert result == 10


#@pytest.mark.parametrize('cli,expected', [
#    (['-o', 'out.xml', 'in.rng'],
#     ),
#])
#def test_main(cli, expected):
#    result = main()
