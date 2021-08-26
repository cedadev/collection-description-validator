from glob import glob

import yaml
from cerberus import Validator

from item_validator.schemas.base import base_schema
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


def err_report(d: dict, v: Validator):
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
    files = glob("descriptions/**/*.yml", recursive=True)

    def load_dir(f: str) -> dict:
        with open(f, 'r') as stream:
            return yaml.safe_load(stream)

    v = Validator()

    for f in files:
        d = load_dir(f)
        t = v.validate(d, base_schema)
        print(f"Validating: {f.split('/')[-1]}..", end="")
        if t:
            print(f"{TextColours.BOLD}{TextColours.OKGREEN}{t}{TextColours.ENDC}")
        if not t:
            print(f"{TextColours.BOLD}{TextColours.FAIL}{t}{TextColours.ENDC}")
            err_report(d, v)


if __name__ == '__main__':
    main()
