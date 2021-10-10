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


from os import getcwd, sep
from os.path import basename
from unittest import TestCase
from regtest import RegressionTestCase

from sphinx_pytype_substitution import substitute, SubstitutionCollection

try:
    from .unicorn import unicorn
except ImportError:
    import unicorn


class SubstitutionCollectionTests(RegressionTestCase):

    def test_extract_module(self):
        sub = SubstitutionCollection().extract_module(unicorn)
        for s in str(sub.shorten_keys()).split("\n"):
            self.assertRegressiveEqual(s)

    def test_replace(self):
        sub = SubstitutionCollection().extract_module(unicorn)
        with open('test/data/source.rst') as source_file:
            source = source_file.read()
        self.assertRegressiveEqual(sub.shorten_keys().replace(source))
        self.assertRegressiveEqual(sub.replace(source))
        new_source = sub.shorten_keys().replace(source)
        with open('test/data/new_source.rst', 'w') as new_source_file:
            new_source_file.write(new_source)

    def test_replace_hash(self):
        sub = SubstitutionCollection(token='#').extract_module(unicorn)
        with open('test/data/source_hash.rst') as source_file:
            source = source_file.read()
        self.assertRegressiveEqual(sub.shorten_keys().replace(source))
        self.assertRegressiveEqual(sub.replace(source))
        new_source = sub.shorten_keys().replace(source)
        with open('test/data/new_source_hash.rst', 'w') as new_source_file:
            new_source_file.write(new_source)

        # self.assertEqual(new_source_file.read(), new_source)
    #self.assertEqual(new_source_file.read(), new_source)


