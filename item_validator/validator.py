# encoding: utf-8
"""
The validation function
"""
__author__ = 'Richard Smith'
__date__ = '02 Dec 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Third-part imports
from cerberus import Validator

# Local imports
from .text_colours import TextColours
from .utils import load_dir


def validate_files(item_descriptions: list, schemamap: dict):
    """
    Creates a cerberus validator.
    The validator first checks that the top level attributes are present.
    If the top level attributes are present, it will inspect the lower levels.
    """
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
