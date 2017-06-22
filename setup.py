#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def requires(filename):
    """Returns a list of all pip requirements

    :param filename: the Pip requirement file (usually 'requirements.txt')
    :return: list of modules
    :rtype: list
    """
    modules = []
    with open(filename, 'r') as pipreq:
        for line in pipreq:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            # if line.startswith('-r'):
            # TODO: what to do here?
            modules.append(line)
    return modules


# ------------------------------------------------------
setup(
    name='rng2doc',
    version='0.1.0',
    license='BSD',
    description='Converts a RELAX NG schema into documentation',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Thomas Schraitle',
    author_email='tom_schr@web.de',
    url='https://bitbucket.com/tomschr/rng2doc',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    keywords=[
        'rng', 'RELAX NG', 'documentation',
    ],

    install_requires=requires('requirements.txt'),

    # Required packages for using "setup.py test"
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-catchlog'],

    entry_points={
        'console_scripts': [
            'rng2doc = rng2doc.cli:main',
        ]
    },
)
