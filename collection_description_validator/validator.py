# encoding: utf-8
"""
The validation function
"""
__author__ = "Richard Smith"
__date__ = "02 Dec 2021"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "richard.d.smith@stfc.ac.uk"

# Third-part imports
from cerberus import Validator

# Local imports
from .utils import load_dir, Messages


def validate_processor(processors: dict, schemamap: dict, processor: str) -> bool:
    """"""
    valid = True
    v = Validator()
    for method in processors:
        try:
            # All processors must have a name defined
            name = method["name"]

            # Find the schema for the given processor
            if schema := schemamap[processor].get(name):

                # Validation failed. Print the errors
                if not v.validate(method, schema):
                    valid = False
                    Messages.print_errors(v)

                # Validation succeeded. Try pre and post processors.
                else:
                    pre_processors_valid = validate_processor(
                        method, schemamap, "pre_processors"
                    )
                    post_processors_valid = validate_processor(
                        method, schemamap, "post_processors"
                    )

                    valid = all([pre_processors_valid, post_processors_valid])
            else:
                # Not having a schema for a given processor isn't an instant fail
                Messages.print_warn(f"WARNING: No schema for {processor}: {name}")
        except KeyError:
            valid = False
            Messages.print_fail(f"Missing {processor} key 'name'")

    return valid


def validate_files(collection_descriptions: list, schemamap: dict):
    """
    Creates a cerberus validator.
    The validator first checks that the top level attributes are present.
    If the top level attributes are present, it will inspect the lower levels.
    """
    v = Validator()
    GLOBAL_PASS = True

    for file in collection_descriptions:
        valid = True
        desc = load_dir(file)

        # GENERAL VALIDATION, BASIC SCHEMA TO VALIDATE THAT ALL IMPORT ATTRIBUTES ARE PRESENT
        print(f"Validating: {file.split('/')[-1]}..", end="")
        if v.validate(desc, schemamap["base_schema"]):

            if extraction_methods := desc.get("collection", {}).get(
                "extraction_methods", {}
            ):
                valid = validate_processor(
                    extraction_methods, schemamap, "extraction_methods"
                )

            if extraction_methods := desc.get("item", {}).get("extraction_methods", {}):
                valid = validate_processor(
                    extraction_methods, schemamap, "extraction_methods"
                )

            if extraction_methods := desc.get("asset", {}).get(
                "extraction_methods", {}
            ):
                valid = validate_processor(
                    extraction_methods, schemamap, "extraction_methods"
                )
        else:
            valid = False
            Messages.print_errors(v)

        # Check all tests were successful
        if valid:
            Messages.print_pass()
        else:
            GLOBAL_PASS = False

    return GLOBAL_PASS
