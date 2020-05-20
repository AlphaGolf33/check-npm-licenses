# check-npm-licenses

A tool for quickly check the license type of installed npm packages

## Requirements

`python > 3.6`

## Usage

```
python3 licenses.py [-h] [-d] [-j] [-p PATH]

optional arguments:
  -h, --help show this help message and exit
  -d, --include-dev include devDependencies from package.json
  -j, --json output in JSON
  -p PATH, --path PATH path to the folder containing the package.json and node_modules/
```
