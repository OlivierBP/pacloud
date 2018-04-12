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
            for dep in db.list_dependencies(package_name, version):
                check_dep(dep)
    check_dep(package_name, version)
    return list

def remove(package_name):
    rmlist = db.list_files(package_name)
    rmlist.reverse()
    
    for paths in rmlist:
        if os.path.isfile(paths):
            rm = os.remove
        elif os.path.isdir(paths):
            remove(paths)
            rm = os.rmdir
