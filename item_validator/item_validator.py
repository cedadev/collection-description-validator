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


def find_file(path: str, f: str) -> str:
    """
    Use glob to find the location of a file in the code with absolute path
    """
    file = glob(f"{path}/**/{f}", recursive=True)
    return file[0]


def main():
    """
    Run Script on file path, check all .yml files in input directory against validation schema and return results.
    """
    parser = argparse.ArgumentParser(description="Validate .yml items")
    parser.add_argument("--filepath", help="Directory or Filepath", type=dir_path, default=os.getcwd(), required=False)
    args = parser.parse_args()
    if args.filepath[-1] != '/':
        args.filepath = args.filepath + '/'
    v = Validator()

    basepath = os.path.dirname(__file__)
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

    item_descriptions = glob(f"{args.filepath}**/*.yml", recursive=True) + \
                        glob(f"{args.filepath}**/*.yaml", recursive=True)

    print_pass = f"{TextColours.BOLD}{TextColours.OKGREEN}Pass{TextColours.ENDC}"
    print_fail = f"{TextColours.BOLD}{TextColours.FAIL}Fail{TextColours.FAIL}"

    for file in item_descriptions:
        valid = True
        desc = load_dir(file)

        # GENERAL VALIDATION, BASIC SCHEMA TO VALIDATE THAT ALL IMPORT ATTRIBUTES ARE PRESENT
        check = v.validate(desc, base_schema)
        print(f"Validating: {file.split('/')[-1]}..", end="")
        if check:
            if desc.get('facets', {}).get('extraction_methods'):
                extraction_methods = desc['facets']['extraction_methods']
                for method in extraction_methods:
                    try:
                        method_name = method['name']
                        if method_name in schemamap['extraction_methods'].keys():
                            schema = schemamap['extraction_methods'].get(method_name)
                            # EXTRACTION_METHOD VALIDATION
                            check = v.validate(method, schema)
                            if check:
                                if method.get('pre_processors'):
                                    pre_processors = method['pre_processors']
                                    for process in pre_processors:
                                        try:
                                            process_name = process['name']
                                            if process_name in schemamap['pre_processors'].keys():
                                                schema = schemamap['pre_processors'].get(process_name)
                                                # PRE-PROCESSOR VALIDATION
                                                check = v.validate(process, schema)
                                                if not check:
                                                    valid = False
                                                    print(f"{print_fail}\n"
                                                          f"{TextColours.FAIL}{v.errors}{TextColours.ENDC}")
                                            else:
                                                valid = False
                                                print(f"{print_fail}\n{TextColours.WARNING}"
                                                      f"WARNING: No such pre_processor: {process_name}{TextColours.ENDC}")
                                        except KeyError:
                                            valid = False
                                            print(f"{print_fail}"
                                                  f"{TextColours.FAIL}Missing pre_process name{TextColours.ENDC}")
                                if method.get('post_processors'):
                                    processors = method['post_processors']
                                    for process in processors:
                                        try:
                                            process_name = process['name']
                                            if process_name in schemamap['post_processors'].keys():
                                                schema = schemamap['post_processors'].get(process_name)
                                                # POST-PROCESSOR VALIDATION
                                                check = v.validate(process, schema)
                                                if not check:
                                                    valid = False
                                                    print(f"{print_fail}\n"
                                                          f"{TextColours.FAIL}{v.errors}{TextColours.ENDC}")
                                            else:
                                                valid = False
                                                print(f"{print_fail}\n{TextColours.WARNING}"
                                                      f"WARNING: No such pre_processor: {process_name}{TextColours.ENDC}")
                                        except KeyError:
                                            valid = False
                                            print(f"{print_fail}"
                                                  f"{TextColours.FAIL}Missing post_process name{TextColours.ENDC}")
                            else:
                                valid = False
                                print(f"{print_fail}\n"
                                      f"{TextColours.FAIL}{v.errors}{TextColours.ENDC}")
                        else:
                            valid = False
                            print(f"{print_fail}\n{TextColours.WARNING}"
                                  f"WARNING: No such extraction_method: {method_name}{TextColours.ENDC}")
                    except KeyError:
                        valid = False
                        print(f"{print_fail}\n"
                              f"{TextColours.FAIL}Missing extract_method name{TextColours.ENDC}")
        else:
            valid = False
            print(f"{print_fail}\n"
                  f"{TextColours.FAIL}{v.errors}{TextColours.ENDC}")
        if valid:
            print(print_pass)


if __name__ == '__main__':
    exit(main())
