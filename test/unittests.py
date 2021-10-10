# -*- coding: utf-8 -*-

# auxilium
# --------
# A Python project for an automated test and deploy toolkit - 100%
# reusable.
#
# Author:   sonntagsgesicht
# Version:  0.1.4, copyright Sunday, 11 October 2020
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)

from sys import path
from logging import basicConfig, INFO, DEBUG
from auxilium.tools.sphinx_tools import html, cleanup
from regtest import RegressionTestCase

from sphinx_pytype_substitution import SubstitutionCollection

basicConfig(level=INFO, format='%(message)s')

try:
    from .test import unicorn
except ImportError:
    import unicorn
    #import test.unicorn as unicorn
    print('')

class SubstitutionCollectionTests(RegressionTestCase):

    def test_extract_module(self):
        sub = SubstitutionCollection(unicorn)
        for s in str(sub.shorten_keys()).split("\n"):
            self.assertRegressiveEqual(s)

    def test_replace(self):
        sub = SubstitutionCollection(unicorn)
        with open('test/data/source.rst') as source_file:
            source = source_file.read()
        self.assertRegressiveEqual(sub.replace(source))
        self.assertRegressiveEqual(sub.shorten_keys().replace(source))

    def test_save_replace(self):
        sub = SubstitutionCollection(unicorn)
        with open('test/data/source.rst') as source_file:
            source = source_file.read()
        new_source = sub.shorten_keys().replace(source)
        with open('test/data/new_source.rst', 'w') as new_source_file:
            new_source_file.write(new_source)

    def test_sphinx(self):
        cleanup(level=DEBUG, path='test/unicorn')
        html(level=INFO, path='test/unicorn')
