from distutils.core import setup
from distutils.extension import Extension
import codecs
import os
import re


def local_file(filename):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), filename), 'r', 'utf-8'
    )

version = re.search(
    "^__version__ = \((\d+), (\d+), (\d+)\)",
    local_file(os.path.join('quantifid', '__init__.py')).read(),
    re.MULTILINE
).groups()

setup(
    name="quantifid",
    version='.'.join(version),
    author='Niel Swart',
    author_email='niel.swart@outlook.com',
    description='Data and updating utilities for backtesting and analysis',
    keywords='python finance quant backtesting data',
    url='https://github.com/pmorissette/bt',
    packages=['quantifid'],
    long_description=local_file('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python'
    ]
)
