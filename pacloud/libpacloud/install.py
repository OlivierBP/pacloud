#!/bin/python3

import libpacloud.database as db
from libpacloud.server import download_package
from libpacloud.config import DB_DIR
import os
import tarfile
import distutils.dir_util
import shutil

# todo: add version and the fact that we want to see a package re-installed if already up-to-date.
def list_dependencies(package_name, version=None):
    list = []
    tested = [] # Stop infinite recursion with co-dependent packages

    #check dependencies
    def check_dep(package_name, version=None):
        if package_name in tested:
            return
        tested.append(package_name)
        installed_version = db.installed_version(package_name)
        dep_package = db.list_dependencies(package_name, version)
        if version == None and installed_version == None and package_name not in list:
            list.append((package_name,version))
        elif (version != None) and (version != installed_version):
            list.append((package_name, version))
        for dep, version in dep_package:
            if dep not in list:
                check_dep(dep, version)

    check_dep(package_name, version)
    return list

def install(package_name, version=None):
    if(version == None):
        version = db.info_package(package_name)["versions"][-1]["number"]
    package_path = "{}/{}/{}-{}.tbz2".format(DB_DIR, package_name, package_name[package_name.find('/')+1:], version)
    if(not os.path.isfile(package_path)):
        print("Downloading {}-{}...".format(package_name, version), end="")
        download_package(package_name, version)
    tar = tarfile.open(package_path)

    # Create list of files that are installed
    rem = tar.getnames()
    rem = [x[1:] for x in rem]
    db.add_files_list(package_name, rem)

    tar.extractall('/tmp/{}'.format(package_name))

    distutils.dir_util.copy_tree('/tmp/{}'.format(package_name),'/')
    db.mark_as_installed(package_name, version)
    shutil.rmtree('/tmp/{}'.format(package_name),'/')

