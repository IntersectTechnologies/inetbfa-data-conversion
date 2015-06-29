# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:59:19 2015

@author: Niel
"""

from distutils.core import setup
from os import path
import codecs
import re

def local_file(filename):
    return codecs.open(
        path.join(path.dirname(__file__), filename), 'r', 'utf-8'
    )

version = re.search(
    "^__version__ = \((\d+), (\d+), (\d+)\)",
    local_file('__init__.py').read(),
    re.MULTILINE
).groups()

setup(
    name="Financial Data Manager",
    version='.'.join(version),
    author='DJ Swart',
    author_email='niel.swart@outlook.com',
    description='Data management application for JSE Equity data',
)
