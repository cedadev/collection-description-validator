from glob import glob

import yaml
from cerberus import Validator

from item_validator.schemas.base import base_schema


class TextColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    files = glob("descriptions/**/*.yml", recursive=True)

    def load_dir(f: str) -> dict:
        with open(f, 'r') as stream:
            return yaml.safe_load(stream)

    v = Validator(base_schema)

    for f in files:
        d = load_dir(f)
        t = v.validate(d)
        print(f"Validating: {f.split('/')[-1]}..", end="")
        if t:
            print(f"{TextColours.BOLD}{TextColours.OKGREEN}{t}{TextColours.ENDC}")
        if not t:
            err = v.errors
            print(f"{TextColours.BOLD}{TextColours.FAIL}{t}{TextColours.ENDC}\n"
                  f"{err}")


if __name__ == '__main__':
    main()
