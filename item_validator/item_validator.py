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
    if os.path.isdir(arg):
        return arg
    else:
        raise NotADirectoryError(arg)


def load_dir(f: str) -> dict:
    with open(f, 'r') as stream:
        return yaml.safe_load(stream)


def err_report(err):
    response = (f"- {err}"
                f"")
    return response


def main():
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
            err = v.errors
            report = err_report(err)
            print(f"{TextColours.BOLD}{TextColours.FAIL}{t}{TextColours.ENDC}\n"
                  f"{report}")


if __name__ == '__main__':
    main()
