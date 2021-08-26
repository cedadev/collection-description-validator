"""Main module."""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import argparse
import os
from glob import glob

import yaml
from cerberus import Validator

import item_validator.schemas.base as base
from item_validator.schemas.extraction_methods import *
from item_validator.schemas.pst_processors import *
from item_validator.schemas.pre_processors import *

subschema_map = {
    'extraction_methods': {
        'regex': regex_schema,
        'header_extract': header_schema,
        'iso19115': iso_schema,
        'xml_extract': xml_schema,
    },
    'processors': {
        'filename_reducer': filename_reducer_schema,
        'ceda_observation': ceda_observation_schema,
        'isodate_processor': isodate_schema,
        'string_join': string_join_schema
    }
}


class TextColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def dir_path(arg: str) -> str:
    """
    Check to make sure input string is valid filepath
    """
    if os.path.isdir(arg):
        return arg
    else:
        raise NotADirectoryError(arg)


def load_dir(f: str) -> dict:
    """
    Method to open .yml file as Python Dictionary
    """
    with open(f, 'r') as stream:
        return yaml.safe_load(stream)


def err_report(d: dict, v: Validator):
    """
    Write an Error Report to identify location and cause of validation Fail

    ==================================
    d: Invalid item
    v: The Validator Class
    - Takes invalid item and return general error report from Cerberus
    - Sub-validates the individual Extraction methods and returns an error report from cerberus of said sub-validation
    - If Extraction methods fails and has processors, sub-validate the processors and return error report
    """
    print(f"{TextColours.FAIL}Error Report\n{v.errors}")
    if d.get('facets', {}).get('extraction_methods'):
        extraction_methods = d['facets']['extraction_methods']
        for method in extraction_methods:
            if method.get('name') in subschema_map['extraction_methods'].keys():
                schema = subschema_map['extraction_methods'].get(method['name'])
                t = v.validate(method, schema['schema'])
                if not t:
                    print(f"Extraction Method: {method.get('name')} Failed!\n"
                          f"{v.errors}")
                    if method.get('pre_processors') or method.get('post_processors'):
                        processors = method.get('pre_processors', []) + method.get('post_processors', [])
                        for processor in processors:
                            if processor.get('name') in subschema_map['processors'].keys():
                                schema = subschema_map['processors'].get(processor['name'])
                                t = v.validate(processor, schema['schema'])
                                if not t:
                                    print(f"Processor: {processor['name']} Failed!\n"
                                          f"{v.errors}")
                            else:
                                print(f"No such processor {processor.get('name', 'or missing name')}")
            else:
                print(f"No such extraction method {method.get('name', 'or missing name')}")
    else:
        print(f"{v.errors}")
    print(f"End Report{TextColours.ENDC}\n")


def main():
    """
    Run Script on file path, check all .yml files in input directory against validation schema and return results.
    """
    parser = argparse.ArgumentParser(description="Validate .yml items")
    parser.add_argument("--dir", help="Directory or Filepath", type=dir_path, default=os.getcwd(), required=False)
    args = parser.parse_args()
    if args.dir[-1] != '/':
        args.dir = args.dir + '/'
    files = glob(f'{args.dir}**/*.yml', recursive=True)
    v = Validator(base.base_schema)

    for f in files:
        d = load_dir(f)
        t = v.validate(d)
        print(f"Validating: {f.split('/')[-1]}..", end="")
        if t:
            print(f"{TextColours.BOLD}{TextColours.OKGREEN}{t}{TextColours.ENDC}")
        if not t:
            print(f"{TextColours.BOLD}{TextColours.FAIL}{t}{TextColours.ENDC}")
            err_report(d, v)


if __name__ == '__main__':
    main()
