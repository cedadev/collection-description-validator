# Item Description Validator

Use schemas to validate item descriptions and assert where
the validator fails.

## Installation

* locate the `item_validator-*.tar.gz` file.
* In the terminal `pip install <filepath>/<item-validator-*.tar.gz>` where the package will be
pip installed.
* Once installed, a new commandline entrypoint will be created: `item-desc-validator`

## Usage

The script when installed provides the command:

* `item-desc-validator --dir <filepath>`: This command will read all **.yml** files in either the `--dir <filepath>`
of your choosing or current working directory if no path is given.
  * `--dir <filepath>`: *optional*, default is current working directory. Location on where to search for **.yml** files.

The command will output the validation test of the yaml files, with either True or False if the files pass the
validator schema. If a file fails the check, the file will be list as False alongside the validator error report where
the checks have failed.

