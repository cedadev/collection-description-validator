#!/usr/bin/env python
"""Tests for `item_validator` package."""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import pytest
import os
from glob import glob
import yaml
from cerberus import Validator


def load_dir(f: str) -> dict:
    with open(f, 'r') as stream:
        return yaml.safe_load(stream)


def find_file(path: str, f: str) -> str:
    file = glob(f"{path}/**/{f}", recursive=True)
    return file[0]


basepath = os.path.dirname(__file__)
basepath = basepath.replace("tests", "item_validator")
base_schema = load_dir(find_file(basepath, "base.yml"))
extraction_files = os.listdir(os.path.join(basepath, "schemas/extraction_methods"))
pre_process_files = os.listdir(os.path.join(basepath, "schemas/pre_processors"))
post_process_files = os.listdir(os.path.join(basepath, "schemas/post_processors"))

schemamap = {
    'base_schema': base_schema,
    'extraction_methods': {os.path.splitext(f)[0]: load_dir(find_file(basepath, f)) for f in extraction_files},
    'pre_processors': {os.path.splitext(f)[0]: load_dir(find_file(basepath, f)) for f in pre_process_files},
    'post_processors': {os.path.splitext(f)[0]: load_dir(find_file(basepath, f)) for f in post_process_files}
}


class TestValidator:

    def test_base(self):
        files = glob(f"{os.path.dirname(__file__)}/descriptions/badc/**/*.yml", recursive=True) +\
                glob(f"{os.path.dirname(__file__)}/descriptions/neodc/**/*.yml", recursive=True)
        v = Validator()
        schema = schemamap['base_schema']
        validatorlist = []
        for f in files:
            d = load_dir(f)
            validatorlist.append(v.validate(d, schema))
        assert all(validatorlist)

    def test_extractions(self):
        files = glob(f"{os.path.dirname(__file__)}/descriptions/badc/**/*.yml", recursive=True) + \
                glob(f"{os.path.dirname(__file__)}/descriptions/neodc/**/*.yml", recursive=True)
        v = Validator()
        schemas = schemamap['extraction_methods']
        validatorlist = []

        for f in files:
            d = load_dir(f)
            if d.get('facets', {}).get('extraction_methods'):
                extracts = d['facets']['extraction_methods']
                for extract in extracts:
                    try:
                        ex_name = extract['name']
                        if ex_name not in schemas.keys():
                            validatorlist.append(False)
                            break
                        schema = schemas.get(ex_name)
                        validatorlist.append(v.validate(extract, schema))
                    except KeyError:
                        validatorlist.append(False)
                        break
        assert all(validatorlist)

    def test_processors(self):
        files = glob(f"{os.path.dirname(__file__)}/descriptions/badc/**/*.yml", recursive=True) + \
                glob(f"{os.path.dirname(__file__)}/descriptions/neodc/**/*.yml", recursive=True)
        v = Validator()
        pre_schemas = schemamap['pre_processors']
        post_schemas = schemamap['post_processors']
        validatorlist = []
        for f in files:
            d = load_dir(f)
            if d.get('facets', {}).get('extraction_methods'):
                extractions = d['facets']['extraction_methods']
                for extract in extractions:
                    if extract.get('pre_processors'):
                        processors = extract['pre_processors']
                        for process in processors:
                            try:
                                process_name = process['name']
                                if process_name not in pre_schemas.keys():
                                    validatorlist.append(False)
                                    break
                                schema = pre_schemas.get(process_name)
                                validatorlist.append(v.validate(process, schema))
                            except KeyError:
                                validatorlist.append(False)
                                break
                    if extract.get('post_processors'):
                        processors = extract['post_processors']
                        for process in processors:
                            try:
                                process_name = process['name']
                                if process_name not in post_schemas.keys():
                                    validatorlist.append(False)
                                    break
                                schema = post_schemas.get(process_name)
                                validatorlist.append(v.validate(process, schema))
                            except KeyError:
                                validatorlist.append(False)
                                break
        assert all(validatorlist)

    @pytest.mark.skip
    def test_base_error(self):
        files = glob(f"{os.path.dirname(__file__)}/descriptions/error/**/*.yml", recursive=True)
        v = Validator()
        schema = schemamap['base_schema']
        validatorlist = []
        for f in files:
            d = load_dir(f)
            validatorlist.append(v.validate(d, schema))
        assert not all(validatorlist)

    def test_invalid_names(self):
        files = glob(f"{os.path.dirname(__file__)}/descriptions/error/**/*.yml", recursive=True)
        v = Validator()
        validatorlist = []
        for f in files:
            d = load_dir(f)
            if d.get('facets', {}).get('extraction_methods'):
                extractions = d['facets']['extraction_methods']
                for ex in extractions:
                    try:
                        if ex['name'] not in schemamap['extraction_methods'].keys():
                            validatorlist.append(False)
                        else:
                            validatorlist.append(True)
                    except KeyError:
                        pass
                    if ex.get('pre_processors'):
                        processors = ex['pre_processors']
                        for process in processors:
                            try:
                                if process['name'] not in schemamap['pre_processors'].keys():
                                    validatorlist.append(False)
                                else:
                                    validatorlist.append(True)
                            except KeyError:
                                pass
                    if ex.get('post_processors'):
                        processors = ex['post_processors']
                        for process in processors:
                            try:
                                if process['name'] not in schemamap['post_processors'].keys():
                                    validatorlist.append(False)
                                else:
                                    validatorlist.append(True)
                            except KeyError:
                                pass
            else:
                validatorlist.append(True)
        assert not all(validatorlist)
