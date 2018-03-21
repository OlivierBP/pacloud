#!/bin/python3

import list_packages
import info_packages
import json
import argparse


def search(name):
    package_names = list_packages()
    corresponding_packages = {}

    for name in package_names:
        if packet_name in name:
            corresponding_packages.append(name)
            package_data = info_packages()
            json.dump(package_data)
    return corresponding_packages


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    packet_name = args.name


if __name__ == '__main__':
    main()
