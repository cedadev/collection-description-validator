# Item Description Validator

Use schemas to validate item descriptions and assert where
the validator fails.

## Installation

* change directory into item_validator and run `python setup.py sdist`,
  this will make a tar.gz zipped package in a new directory called dist.
* locate the `item_validator-*.tar.gz` file.
* In the terminal `pip install <filepath>/<item-validator-*.tar.gz>` where the package will be
pip installed.
* Once installed, a new commandline entrypoint will be created: `item-desc-validator`

## Usage

### Commands
The script when installed provides the command:

* `item-desc-validator --dir <filepath>`: This command will read all **.yml** files in either the `--dir <filepath>`
of your choosing or current working directory if no path is given.
  * `--dir <filepath>`: *optional*, default is current working directory. Location on where to search for **.yml** files.

The command will output the validation test of the yaml files, with either True or False if the files pass the
validator schema. If a file fails the check, the file will be list as False alongside the validator error report where
the checks have failed.

### Adding Schemas
To add more validation schemas of extraction_methods, pre_processors & post_processors, they can be added as **.yml**
files under `item_validator/schemas/` in the appropriate directory.

The convention of the **.yml** validation schemas uses [Cerberus](https://docs.python-cerberus.org/en/stable/)
and follows the file name should be <name>.yml where name is the name attribute of the validator.

# Workflow

This script will locate and import a schema map containing a basic validation schema, all available extraction method,
post and pre processor schemas.
Then find the relevant .yml files in current working directory or from console argument to validate.
Validation takes the process of:
- validate against base schematic
- if there are extraction methods, validate them
- if there are processors, validate them

The validator will catch three types of invalidation:

- general validation failed with cerberus Validator, does not follow schema.
- missing names, can not find a schema to validate against as there is no name in the file.
- non-existent name, the name in the file does not match against any validation schemas.

## Pre-Commit Config

If to run on pre-commit hook, add the following to the
.pre-commit-config.yaml file:

```yaml
repos:
  - repo: https://github.com/Mahir-Sparkess/item_validator.git
    rev: v1.0.3
    hooks:
      - id: item-desc-validator
        args: [--filepath=<FILEPATH>]
```

where args are **optional** and <FILEPATH> is the location
of the item descriptions.
