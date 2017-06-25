# Standard Library
from unittest.mock import patch

# Third Party Libraries
import pytest

# My Stuff
from rng2doc.cli import checkargs, main, parsecli


@pytest.mark.parametrize('cli,expected', [
  (['-o', 'out.xml', 'in.rng'],
   {'RNGFILE': 'in.rng',
    '--output': 'out.xml'}
   ),
  (['-v', '-o', 'out.xml', 'in.rng'],
   {'-v': 1,
    'RNGFILE': 'in.rng',
    '--output': 'out.xml'}
   ),
  (['-vv', '-o', 'out.xml', 'in.rng'],
   {'-v': 2,
    'RNGFILE': 'in.rng',
    '--output': 'out.xml'}
   ),
  (['-vvv', '-o', 'out.xml', 'in.rng',],
   {'-v': 3,
    'RNGFILE': 'in.rng',
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
    assert checkargs({'RNGFILE': 'fake.rng'}) is None


@patch('rng2doc.cli.os.path.exists')
def test_checkargs_notfound_rng(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        checkargs({'RNGFILE': 'fake.rng'})

def test_checkargs_with_DocoptExit():
    from docopt import DocoptExit
    with pytest.raises(DocoptExit):
        checkargs({'RNGFILE': None})
