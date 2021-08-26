#!/usr/bin/env python
"""Tests for `item_validator` package."""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

from io import StringIO
import sys
from unittest import TestCase
from glob import glob
from cerberus import Validator
from item_validator.item_validator import base, load_dir, err_report


class TestValidation(TestCase):

    def test_badc(self):
        """
        Test all basc examples pass
        """
        files = glob("descriptions/badc/**/*.yml", recursive=True)
        for f in files:
            d = load_dir(f)
            v = Validator(base.base_schema)
            t = v.validate(d)
            self.assertTrue(t)

    def test_neodc(self):
        """
        Test all neodc examples pass
        """
        files = glob("descriptions/neodc/**/*.yml", recursive=True)
        for f in files:
            d = load_dir(f)
            v = Validator(base.base_schema)
            t = v.validate(d)
            self.assertTrue(t)

    def test_invalid_extract(self):
        """
        Test sub-validate extraction method given invalid method
        """
        files = glob("descriptions/error/invalid_extracts.yml", recursive=True)
        for f in files:
            capture = StringIO()
            d = load_dir(f)
            v = Validator(base.base_schema)
            t = v.validate(d)
            sys.stdout = capture
            err_report(d, v)
            capture_out = capture.getvalue().split('\n')
            self.assertFalse(t)
            self.assertTrue('No such extraction method extract_invalid' in capture_out)

    def test_invalid_processor(self):
        """
        Test sub-validate processors if given invalid processor
        """
        files = glob("descriptions/error/invalid_processor.yml", recursive=True)
        for f in files:
            capture = StringIO()
            d = load_dir(f)
            v = Validator(base.base_schema)
            t = v.validate(d)
            sys.stdout = capture
            err_report(d, v)
            capture_out = capture.getvalue().split('\n')
            self.assertFalse(t)
            self.assertTrue('No such processor pre_invalid' in capture_out)
            self.assertTrue('No such processor post_invalid' in capture_out)

    def test_invalid_dependencies(self):
        """
        General test check missing dependencies
        """
        files = glob("descriptions/error/invalid_dependencies.yml", recursive=True)
        for f in files:
            capture = StringIO()
            d = load_dir(f)
            v = Validator(base.base_schema)
            t = v.validate(d)
            sys.stdout = capture
            err_report(d, v)
            capture_out = capture.getvalue().split('\n')
            self.assertFalse(t)
            self.assertTrue('{\'facets\': ["field \'defaults\' is required"]}' in capture_out)
