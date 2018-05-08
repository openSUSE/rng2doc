# Standard Library
from unittest.mock import patch

# Third Party Libraries
import pytest
from lxml import etree

# My Stuff
from rng2doc.cli import checkargs, main, parsecli


@pytest.mark.parametrize('cli,expected', [
    (['-o', 'out.xml', 'in.rng'],
     {'RNGFILE': 'in.rng',
      '--output-format': 'xml',
      '--output': 'out.xml'}
    ),
    (['-v', '-o', 'out.xml', 'in.rng'],
     {'-v': 1,
      'RNGFILE': 'in.rng',
      '--output-format': 'xml',
      '--output': 'out.xml'}
    ),
    (['-vv', '-o', 'out.xml', 'in.rng'],
     {'-v': 2,
      'RNGFILE': 'in.rng',
      '--output-format': 'xml',
      '--output': 'out.xml'}
    ),
    (['-vvv', '-o', 'out.xml', 'in.rng',],
     {'-v': 3,
      'RNGFILE': 'in.rng',
      '--output-format': 'xml',
      '--output': 'out.xml'}
    ),
    (['--output-format', 'html', '-o', 'out.xml', 'in.rng',],
     {'RNGFILE': 'in.rng',
      '--output-format': 'html',
      '--output': 'out.xml'}
    ),
])
def test_parsecli(cli, expected):
    result = parsecli(cli)
    # Create set difference and only compare this with the expected dictionary
    assert {item: result.get(item, None) for item in expected} == expected


@patch('rng2doc.cli.os.path.exists')
def test_checkargs_found_rng(mock_exists):
    mock_exists.return_value = True
    assert checkargs({'RNGFILE': 'fake.rng', '--output-format': 'xml'}) is None


@patch('rng2doc.cli.os.path.exists')
def test_checkargs_notfound_rng(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        checkargs({'RNGFILE': 'fake.rng', '--output-format': 'xml'})


@patch('rng2doc.cli.os.path.exists')
def test_checkargs_unknown_output_format(mock_exists):
    mock_exists.return_value = True
    with pytest.raises(RuntimeError):
        checkargs({'RNGFILE': 'fake.rng', '--output-format': 'test'})


def test_checkargs_with_DocoptExit():
    from docopt import DocoptExit
    with pytest.raises(DocoptExit):
        checkargs({'RNGFILE': None, '--output-format': 'xml'})
