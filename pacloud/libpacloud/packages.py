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
    pass
