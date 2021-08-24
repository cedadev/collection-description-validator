import yaml
from cerberus import Validator
from item_validator.schemas.base import base_schema
from glob import glob


files = glob("descriptions/**/*.yml", recursive=True)
examples = []

for f in files:
    with open(f, 'r') as stream:
        examples.append(yaml.safe_load(stream))

v = Validator(base_schema)

for (item, filename) in zip(examples, files):
    t = v.validate(item)
    if not t:
        print(f'{t} for {filename}:\n'
              f'-   {v.errors}')
    else:
        print(f'{t} for {filename}')


