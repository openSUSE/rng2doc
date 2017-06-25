# Standard Library
import logging
import os
from unittest.mock import patch

# Third Party Libraries
import pytest
from docopt import DocoptExit

# My Stuff
import rng2doc
from rng2doc.cli import main
from rng2doc.common import errorcode

# log = logging.getLogger(rng2doc.__package__)


def test_main():
    assert main([]) == errorcode(DocoptExit())


def test_invalid():
    assert main(["", "--wrong-option"]) == errorcode(DocoptExit())


def test_help():
    with pytest.raises(SystemExit):
        main(["", "--help"])


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
    from docopt import DocoptExit
    mock_exists.return_value = False
    result = main([rng2doc.__package__, "fake.rng"])
    assert result == errorcode(DocoptExit())


@patch('rng2doc.cli.parsecli')
def test_main_with_KeyboardInterrupt(mock_parsecli):
    mock_parsecli.side_effect = KeyboardInterrupt
    result = main([rng2doc.__package__, "fake.rng"])
    assert result == errorcode(KeyboardInterrupt())


@patch('rng2doc.cli.checkargs')
@patch('rng2doc.cli.parsecli')
@patch('rng2doc.cli.process')
def test_main_with_success_of_process(mock_process, mock_parsecli, mock_checkargs):
    mock_process.return_value = 1000
    mock_parsecli.return_value = {'RNGFILE': 'fake.rng',
                                  '--version': False,
                                  '-v': 0,
                                  '--output': None}
    mock_checkargs.return_value = None

    result = main([rng2doc.__package__, "fake.rng"])
    assert result == 1000

@pytest.mark.skip
@patch('rng2doc.cli.checkargs')
def test_main_with_FileNotFound(mock_checkargs):
    mock_checkargs.side_effect = FileNotFoundError()
    print(">>>>")
    result = main([rng2doc.__package__, "fake.rng"])
    assert mock_checkargs.called
    assert result == errorcode(FileNotFoundError())


#@pytest.mark.parametrize('cli,expected', [
#    (['-o', 'out.xml', 'in.rng'],
#     ),
#])
#def test_main(cli, expected):
#    result = main()
