"""Main module."""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
import sys
from glob import glob

from cerberus import Validator

from item_validator.utils import load_dir, dir_path, get_filepath_arg, get_schemamap
from item_validator.text_colours import TextColours


def main(filepath: str = None):
    """
    Run Script on file path, check all .yml files in input directory against validation schema and return results.
    """
    if filepath:
        dir_path(filepath)
    else:
        filepath = get_filepath_arg(sys.argv[1:])

    basepath = os.path.dirname(__file__)
    schemamap = get_schemamap(basepath)

    item_descriptions = glob(f"{filepath}**/*.yml", recursive=True) + glob(f"{filepath}**/*.yaml", recursive=True)

    GLOBAL_PASS = validate_files(item_descriptions, schemamap)

    # Return a non-zero exit code if any of the validation tests fail, so that it can work in CI
    if not GLOBAL_PASS:
        exit(1)


def validate_files(item_descriptions: list, schemamap: dict):
    v = Validator()
    GLOBAL_PASS = True
    print_pass = f"{TextColours.BOLD}{TextColours.OKGREEN}Pass{TextColours.ENDC}"
    print_fail = f"{TextColours.BOLD}{TextColours.FAIL}Fail{TextColours.FAIL}"

    for file in item_descriptions:
        valid = True
        desc = load_dir(file)

        # GENERAL VALIDATION, BASIC SCHEMA TO VALIDATE THAT ALL IMPORT ATTRIBUTES ARE PRESENT
        print(f"Validating: {file.split('/')[-1]}..", end="")
        if v.validate(desc, schemamap['base_schema']):
            if extraction_methods := desc.get('facets', {}).get('extraction_methods'):
                for method in extraction_methods:
                    try:
                        method_name = method['name']
                        if method_name in schemamap['extraction_methods'].keys():
                            schema = schemamap['extraction_methods'].get(method_name)
                            # EXTRACTION_METHOD VALIDATION
                            if v.validate(method, schema):
                                if method.get('pre_processors'):
                                    pre_processors = method['pre_processors']
                                    for process in pre_processors:
                                        try:
                                            process_name = process['name']
                                            if process_name in schemamap['pre_processors'].keys():
                                                schema = schemamap['pre_processors'].get(process_name)
                                                # PRE-PROCESSOR VALIDATION
                                                if not v.validate(process, schema):
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
        else:
            GLOBAL_PASS = False

    return GLOBAL_PASS


if __name__ == '__main__':
    main()
