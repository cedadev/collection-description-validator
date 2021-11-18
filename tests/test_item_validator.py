#!/usr/bin/env python
"""Tests for `item_validator` package."""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
from glob import glob
from pathlib import Path

from item_validator.utils import get_schemamap
from item_validator.validator_script import validate_files

root = Path(os.path.abspath(__file__)).parent.parent
basepath = os.path.join(root, 'item_validator')

schemamap = get_schemamap(basepath)


class TestValidator:

    def test_valid(self):
        item_descriptions = glob(f"{os.path.join(root, 'tests', 'descriptions')}/badc/**/*.yml", recursive=True) + glob(
            f"{os.path.join(root, 'tests', 'descriptions')}/neodc/**/*.yml", recursive=True)
        assert validate_files(item_descriptions, schemamap)

    def test_invalid(self):
        item_descriptions = glob(f"{os.path.join(root, 'tests', 'descriptions')}/error/**/*.yml", recursive=True)
        assert not validate_files(item_descriptions, schemamap)

