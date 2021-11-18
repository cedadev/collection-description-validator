"""Utility module"""

__author__ = """Mahir Rahman"""
__contact__ = 'kazi.mahir@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import argparse
import os
from glob import glob

import yaml


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


def get_filepath_arg(args):
    parser = argparse.ArgumentParser(description="Validate .yml items")
    parser.add_argument("filepath", help="Directory or Filepath", type=dir_path, default=os.getcwd())
    args = parser.parse_args(args)
    if args.filepath[-1] != '/':
        args.filepath = args.filepath + '/'
    return args.filepath


def get_schemamap(basepath):
    base_schema = load_dir(find_file(basepath, "base.yml"))
    extraction_files = os.listdir(os.path.join(basepath, "schemas", "extraction_methods"))
    pre_process_files = os.listdir(os.path.join(basepath, "schemas", "pre_processors"))
    post_process_files = os.listdir(os.path.join(basepath, "schemas", "post_processors"))

    schemamap = {
        'base_schema': base_schema,
        'extraction_methods': {os.path.splitext(f)[0]: load_dir(find_file(basepath, f)) for f in extraction_files},
        'pre_processors': {os.path.splitext(f)[0]: load_dir(find_file(basepath, f)) for f in pre_process_files},
        'post_processors': {os.path.splitext(f)[0]: load_dir(find_file(basepath, f)) for f in post_process_files}
    }
    return schemamap
