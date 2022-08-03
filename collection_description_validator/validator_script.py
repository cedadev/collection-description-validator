"""Main module."""

__author__ = """Mahir Rahman"""
__contact__ = "kazi.mahir@stfc.ac.uk"
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
import sys
from glob import glob


from collection_description_validator.utils import (
    dir_path,
    get_filepath_arg,
    get_schemamap,
)
from collection_description_validator.validator import validate_files


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

    collection_descriptions = glob(f"{filepath}**/*.yml", recursive=True) + glob(
        f"{filepath}**/*.yaml", recursive=True
    )

    full_pass = validate_files(collection_descriptions, schemamap)

    # Return a non-zero exit code if any of the validation tests fail, so that it can work in CI
    if not full_pass:
        exit(1)


if __name__ == "__main__":
    main()
