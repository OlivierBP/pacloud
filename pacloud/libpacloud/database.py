#!/usr/bin/python

import os
import json

from config import DB_DIR

PACKAGE_DIR = lambda pkg_name: '{}{}'.format(DB_DIR, pkg_name)
METADATA_FILE = lambda pkg_name: '{}/metadata.json'.format(PACKAGE_DIR(pkg_name))

def list_packages():
    packages = os.listdir(DB_DIR)
    return packages

def info_package(package_name):
    metadata_file = open(METADATA_FILE(package_name), 'r')
    data = json.load(metadata_file)
    metadata_file.close()
    return data

# Just a helper function to rewrite a package metadata, not to be called by other modules.
def rewrite_metadata(package_name, metadata):
    metadata_file = open(METADATA_FILE(package_name), 'w+')
    metadata_file.write(json.dumps(metadata))
    metadata_file.close()

def add_package(package_name, metadata):
    os.makedirs(PACKAGE_DIR(package_name))
    rewrite_metadata(package_name, metadata)

def remove_package(package_name):
    files = os.listdir(PACKAGE_DIR(package_name))
    for file in files:
        os.remove('{}/{}'.format(PACKAGE_DIR(package_name), file))
    os.removedirs(PACKAGE_DIR(package_name))

def modify_package(package_name, new_metadata):
    current_metadata = info_package(package_name)
    # Updating the database doesn't have to change the state of installed packages
    if('installed' in current_metadata):
        new_metadata['installed'] = current_metadata['installed']
    rewrite_metadata(package_name, new_metadata)

def mark_as_installed(package_name, version):
    metadata = info_package(package_name)
    metadata['installed'] = version
    rewrite_metadata(package_name, metadata)

def mark_as_uninstalled(package_name):
    metadata = info_package(package_name)
    metadata.pop('installed', None)
    rewrite_metadata(package_name, metadata)

if __name__ == "__main__":
    mark_as_installed("example", "2.4")
