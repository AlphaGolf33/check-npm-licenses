#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import os.path
import sys

def print_line(name, license):
    # customize the display here if you want
    print(f"{name}: {license}")

def get_license_type(package, node_modules_path):
    package_json_path = os.path.join(node_modules_path, package, "package.json")
    # Read package.json license field
    if (os.path.isfile(package_json_path)):
        with open(package_json_path) as package_json:
            package_json_data = json.load(package_json)
            if "license" in package_json_data:
                if "type" in package_json_data["license"]:
                    return package_json_data["license"]["type"]
                else:
                    return package_json_data["license"]

    # If package.json or "license" key not found
    return "n/a"

def main():
    # Check python version
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 6):
        print("ERROR: This program requires at least python 3.6")
        exit(1)

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--include-dev", help="include devDependencies from package.json", action="store_true")
    parser.add_argument("-j", "--json", help="output in JSON", action="store_true")
    parser.add_argument("-p", "--path", help="path to the folder containing the package.json and node_modules/")
    args = parser.parse_args()

    # Get the path to the project, default is current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    if args.path:
        path = os.path.join(current_dir, args.path)
    else:
        path = current_dir

    # Check if package.json exists
    package_json_path = os.path.join(path, "package.json")
    if (not(os.path.isfile(package_json_path))):
        print(f"ERROR: Unable to find {package_json_path}\nTry with --path argument")
        exit(1)

    # Check if node_modules exists
    node_modules_path = os.path.join(path, "node_modules")
    if (not(os.path.isdir(node_modules_path))):
        print(f"ERROR: Unable to find {node_modules_path}\nDid you run `npm install` ?")
        exit(1)

    # Store output
    licenses = []

    # Read package.json
    with open(package_json_path) as package_json:
        package_json_data = json.load(package_json)

        # Check if "dependencies" key exists
        if "dependencies" not in package_json_data:
            print(f"ERROR: Unable to find `dependencies` field in {package_json_path}")
            exit(1)

        # dependencies
        for dependecy in package_json_data["dependencies"]:
            license_type = get_license_type(dependecy, node_modules_path)
            if args.json:
                licenses.append({"package": dependecy, "license": license_type})
            else:
                print_line(dependecy, license_type)

        # devDependencies
        if args.include_dev and "devDependencies" in package_json_data:
            for dependecy in package_json_data["devDependencies"]:
                license_type = get_license_type(dependecy, node_modules_path)
                if args.json:
                    licenses.append({"package": dependecy, "license": license_type})
                else:
                    print_line(dependecy, license_type)
    
    # Print JSON if json argument
    if args.json:
        print(json.dumps(licenses, indent=2))

if __name__ == "__main__":
    main()

