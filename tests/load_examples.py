import yaml
from glob import glob

files = glob("tests/descriptions/**.yml")
examples = []

for f in files:
    with open(f, 'r') as stream:
        examples.append(yaml.safe_load(stream))
