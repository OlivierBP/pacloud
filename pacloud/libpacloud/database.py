#!/usr/bin/python

import os
import json

DB_DIRECTORY = '/var/lib/pacloud/db/'

def list_packages():
    packages = os.listdir(DB_DIRECTORY)
    return packages

def info_package(package_name):
    metadata_file = open('{}{}/metadata.json'.format(DB_DIRECTORY, package_name), 'r')
    data = json.load(metadata_file)
    metadata_file.close()
    return data

# Just a helper function to rewrite a packae metadata, not to be called by other modules.
def rewrite_metadata(package_name, metadata):
    metadata_file = open('{}/metadata.json'.format(DB_DIRECTORY, package_name), 'w+')
    metadata_file.write(json.dumps(metadata))
    metadata_file.close()

def add_package(package_name, metadata):
    os.makedirs('{}{}'.format(DB_DIRECTORY, package_name))
    rewrite_metadata(package_name, metadata)

def remove_package(package_name):
    files = os.listdir('{}{}'.format(DB_DIRECTORY, package_name))
    for file in files:
        os.remove('{}{}/{}'.format(DB_DIRECTORY, package_name, file))
    os.removedirs('{}{}'.format(DB_DIRECTORY, package_name))

def modify_package(package_name, new_metadata):
    current_metadata = info_package(package_name)
    if('installed' in current_metadata):
        installed_version = current_metadata['installed']
    if 'installed_version' in locals():
        new_metadata['installed'] = installed_version
    rewrite_metadata(package_name, new_metadata)

def mark_as_installed(package_name, version):
    metadata = info_package(package_name)
    metadata['installed'] = version
    rewrite_metadata(package_name, metadata)

def mark_as_uninstalled(package_name):
    metadata = info_package(package_name)
    metadata.pop('installed', None)
    rewrite_metadata(package_name, metadata)

