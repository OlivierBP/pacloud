#!/usr/bin/python

import libpacloud.database as db
from libpacloud.config import DB_DIR
from libpacloud.server import download_package

import os
import tarfile
import distutils.dir_util
import shutil

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

def _progress_tar(members):
    index = 0
    for m in members:
        index = index + 1
        yield index

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
    yield len(rem)
    members = tar.getmembers()
    index = 0
    for member in members:
        index = index + 1
        tar.extract(member, '/tmp/{}-{}'.format(package_name, version))
        yield index
    #tar.extractall('/tmp/{}-{}'.format(package_name, version), members=_progress_tar(tar))
    tar.close()
    distutils.dir_util.copy_tree('/tmp/{}-{}'.format(package_name, version),'/')

    shutil.rmtree('/tmp/{}-{}'.format(package_name, version),'/')
