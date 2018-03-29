#!/bin/python3

import libpacloud.database as db
from libpacloud.server import download_package
from libpacloud.config import DB_DIR
import os
import tarfile
import distutils.dir_util


def list_dependencies(package_name, version=None):
    list = []

    #check dependencies
    def check_dep(package_name, version=None):
        installed_version = db.installed_version(package_name)
        dep_package = db.list_dependencies(package_name, version)
        if package_name not in list:
            list.append(package_name)
        elif (version != None) and (version != installed_version):
            list.append(package_name)
        for dep in dep_package:
            if dep not in list and package_name not in list:
                check_dep(dep)
            if package_name not in list:
                list.append(package_name) 

    check_dep(package_name)
    return list



def install(package_name, version=None):
    if(version == None):
        version = db.info_package(package_name)["versions"][0]["number"]
    package_path = "{}/{}/{}-{}.tbz2".format(DB_DIR, package_name, package_name, version)
    if(not os.path.isfile(package_path)):
        print("Downloading {}-{}...".format(package_name, version), end="")
        download_package(package_name, version)
    tar = tarfile.open(package_path)
    tar.extractall('/tmp/{}'.format(package_name))

    """
    path = os.path.abspath('/tmp/{}'.format(package_name))

    if not os.path.exists(path):
        os.makedirs(path,exist_ok = True)
"""
    distutils.dir_util.copy_tree('/tmp/{}'.format(package_name),'/')
    db.mark_as_installed(package_name, version)

