#!/bin/python3

from server import pkg
from database import list_packages
import urllib.request
import os
import zipfile
import shutil


list = []
listdb = list_packages()

#check dependencies
def check_dep(pkg):
    if len(pkg.dep == 0) and pkg not in listdb:
        list.append(pkg)
    else:
        for dep in pkg.dep:
            if pkg not in listdb:
                list.appen(pkg)
            if dep not in listdb:
                check.dep(dep)
    return list



def install(package_name, version):
    zip_ref = zipfile.ZipFile('"{}/{}/{}-{}.tbz2".format(DB_DIR, package_name, package_name, version)','r')
    zip = zip_ref.extractall('./tmp')
    zip_ref.close()
    
    path = os.abspath(zip)

    if not os.path.exists(path):
        os.makedirs(path,exist_ok = True)

    distutils.dir_util.copy_tree(zip,path) 
    return True


if _name_ == '_main_':
    main()
