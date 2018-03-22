#!/bin/python3

import libpacloud.database as db
from libpacloud.config import DB_DIR
import os
import tarfile
import distutils.dir_util


def list_dependencies(package_name, version=None):
    list = []

    #check dependencies
    def check_dep(package_name):
        package = db.info_package(package_name)
        if len(package["versions"][0]["dependencies"]) == 0 and package["name"] not in list:
            list.append(package["name"])
        else:
            for dep in package["versions"][0]["dependencies"]:
                if package["name"] not in list:
                    list.append(package["name"])
                if dep not in list:
                    check_dep(dep)

    check_dep(package_name)
    return list



def install(package_name, version):
    tar = tarfile.open("{}/{}/{}-{}.tbz2".format(DB_DIR, package_name, package_name, version))
    tar.extractall('/tmp/{}'.format(package_name))

    """
    path = os.path.abspath('/tmp/{}'.format(package_name))

    if not os.path.exists(path):
        os.makedirs(path,exist_ok = True)
"""
    distutils.dir_util.copy_tree('/tmp/{}'.format(package_name),'/') 
    db.mark_as_installed(package_name, version)

