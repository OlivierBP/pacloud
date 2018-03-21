#!/bin/python3

from libpacloud.database import list_packages, info_package

def search(package_name):
    package_names = list_packages()
    corresponding_packages = []

    for name in package_names:
        if package_name in name:
            package_data = info_package(name)
            corresponding_packages.append(package_data)
    return corresponding_packages

