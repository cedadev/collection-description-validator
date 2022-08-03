#!/usr/bin/env python
"""Tests for `collection_description_validator` package."""

__author__ = """Mahir Rahman"""
__contact__ = "kazi.mahir@stfc.ac.uk"
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
from glob import glob
from pathlib import Path

from collection_description_validator.utils import get_schemamap
from collection_description_validator.validator import validate_files

root = Path(os.path.abspath(__file__)).parent.parent
basepath = os.path.join(root, "collection_description_validator")

schemamap = get_schemamap(basepath)


class TestValidator:
    def test_valid(self):
        collection_descriptions = glob(
            f"{os.path.join(root, 'tests', 'descriptions')}/badc/**/*.yml",
            recursive=True,
        )
        assert validate_files(collection_descriptions, schemamap)

    def test_warn(self):
        collection_descriptions = glob(
            f"{os.path.join(root, 'tests', 'descriptions')}/warn/**/*.yml",
            recursive=True,
        )
        assert validate_files(collection_descriptions, schemamap)

    def test_invalid(self):
        collection_descriptions = glob(
            f"{os.path.join(root, 'tests', 'descriptions')}/error/**/*.yml",
            recursive=True,
        )
        assert not validate_files(collection_descriptions, schemamap)
