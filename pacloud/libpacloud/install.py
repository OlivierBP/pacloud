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
    def check_dep(package_name):
        package = db.info_package(package_name)
        try:
            if(version != None or package["versions"][0]["number"] != package["installed"]):
                list.append(package["name"])
                for dep in package["versions"][0]["dependencies"]:
                    check_dep(dep)
        except KeyError:
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
    print(distutils.dir_util.copy_tree('/tmp/{}'.format(package_name),'/'))
    db.mark_as_installed(package_name, version)

