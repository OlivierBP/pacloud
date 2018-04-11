#!/usr/bin/python

import os
import json

from libpacloud.config import DB_DIR

PACKAGE_DIR = lambda pkg_name: '{}{}'.format(DB_DIR, pkg_name)
METADATA_FILE = lambda pkg_name: '{}/metadata.json'.format(PACKAGE_DIR(pkg_name))

def list_packages():
    list = []
    for folder in os.listdir(DB_DIR):
        list.extend(['{}/{}'.format(folder, subfolder) for subfolder in os.listdir('{}/{}'.format(DB_DIR, folder))])
    return sorted(list)

def info_package(package_name):
    return json.load(open(METADATA_FILE(package_name), 'r'))

def _parse_dependencies(list, dep):
    if '(' not in dep:
        list.append(dep)

def list_dependencies(package_name, version=None):
    versions = info_package(package_name)["versions"]
    dependencies = []
    list = []
    if(version == None):
        dependencies = versions[-1]["dependencies"]
    else:
        for v in versions:
            if(v["number"] == version):
                dependencies = v["dependencies"]
                break
    for dep in dependencies:
        _parse_dependencies(list, dep)
    print(list)
    return list

def installed_version(package_name):
    try:
        return info_package(package_name)["installed"]
    except KeyError:
        return None

# Just a helper function to rewrite a package metadata, not to be called by other modules.
def _rewrite_metadata(package_name, metadata):
    metadata_file = open(METADATA_FILE(package_name), 'w+')
    metadata_file.write(json.dumps(metadata))
    metadata_file.close()

def add_package(package_name, metadata):
    os.makedirs(PACKAGE_DIR(package_name))
    _rewrite_metadata(package_name, metadata)

def remove_package(package_name):
    files = os.listdir(PACKAGE_DIR(package_name))
    for file in files:
        os.remove('{}/{}'.format(PACKAGE_DIR(package_name), file))
    os.removedirs(PACKAGE_DIR(package_name))

def modify_package(package_name, new_metadata):
    current_metadata = info_package(package_name)
    # Updating the database doesn't have to change the state of installed packages and required_by
    if('installed' in current_metadata):
        new_metadata['installed'] = current_metadata['installed']
    if('required_by' in current_metadata):
        new_metadata['required_by'] = current_metadata['required_by']
    _rewrite_metadata(package_name, new_metadata)

def mark_as_installed(package_name, version):
    metadata = info_package(package_name)
    metadata['installed'] = version
    for available_version in metadata['versions']:
        if(available_version['number'] == version):
            for dependency in available_version['dependencies']:
                dependency_name = dependency#[:max(-1,min(dependency.find('>'), dependency.find('=')))]
                _mark_as_required_by(dependency_name, package_name)
    _rewrite_metadata(package_name, metadata)


def mark_as_uninstalled(package_name):
    metadata = info_package(package_name)
    for available_version in metadata['versions']:
        if(available_version['number'] == metadata['installed']):
            for dependency in available_version['dependencies']:
                dependency_name = dependency#[:max(-1,min(dependency.find('>'), dependency.find('=')))]
                _remove_required_by(dependency_name, package_name)
    metadata.pop('installed', None)
    _rewrite_metadata(package_name, metadata)

def _mark_as_required_by(package_name, required_by):
    metadata = info_package(package_name)
    try:
        if(not required_by in metadata['required_by']):
            metadata['required_by'].append(required_by)
    except KeyError:
        metadata['required_by'] = []
        metadata['required_by'].append(required_by)
    _rewrite_metadata(package_name, metadata)

def _remove_required_by(package_name, required_by):
    metadata = info_package(package_name)
    metadata['required_by'].remove(required_by)
    _rewrite_metadata(package_name, metadata)

def add_files_list(package_name, files_list):
    tree = open(PACKAGE_DIR(package_name) + '/tree', 'w')
    for file in files_list:
        tree.write(file + '\n')
    tree.close()

def list_files(package_name):
    tree = open(PACKAGE_DIR(package_name) + '/tree', 'r')
    files = [x.strip() for x in tree.readlines()]
    tree.close()
    return files
