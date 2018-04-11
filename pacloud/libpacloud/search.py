#!/bin/python3

import libpacloud.database as db

def search(package_name):
    package_names = db.list_packages()
    corresponding_packages = []

    for name in package_names:
        if package_name in name:
            package_data = db.info_package(name)
            corresponding_packages.append(package_data)
    return corresponding_packages

def list_packages():
    return db.list_packages()
