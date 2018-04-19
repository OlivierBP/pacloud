#!/usr/bin/python

import libpacloud.database as db

import os
import tarfile
import distutils.dir_util

def list_dependencies(package_name, version=None):
    list = []

    def check_dep(package_name, version=None):
        if package_name not in list:
            list.append(package_name)
            for dep, version in db.list_dependencies(package_name, version):
                check_dep(dep, version)
    check_dep(package_name, version)
    return list

def remove(package_name):
    rmlist = db.list_files(package_name)
    rmlist.reverse()
    remaining_files = len(rmlist)
    yield remaining_files
    index = 0

    for paths in rmlist:
        index = index+1
        if os.path.isfile(paths):
            os.remove(paths)
        elif os.path.isdir(paths):
            try:
                os.rmdir(paths)
            except OSError: # Directory not empty
                pass
        yield index
