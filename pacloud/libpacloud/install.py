#!/bin/python3

import libpacloud.database as db
import libpacloud.packages as pkg

# todo: add version and the fact that we want to see a package re-installed if already up-to-date.
def list_dependencies(package_name, version=None):
    list = []
    tested = [] # Stop infinite recursion with co-dependent packages

    #check dependencies
    def check_dep(package_name, version=None, force=False):
        if force:
            list.append((package_name, db._find_package_version(None, package_name, version)))
        if package_name in tested:
            return
        tested.append(package_name)
        installed_version = db.installed_version(package_name)
        dep_package = db.list_dependencies(package_name, version)
        if version == None and installed_version == None and (package_name, None) not in list:
            list.append((package_name, db._find_package_version(None, package_name, version)))
        elif (version != None) and (version != installed_version) and (package_name, version) not in list:
            list.append((package_name, version))
        for dep, version in dep_package:
            if dep not in list:
                check_dep(dep, version)

    check_dep(package_name, version, force=True)
    return list

def install(package_name, version=None):
    for file_installed in pkg.install(package_name, version):
        yield file_installed
    db.mark_as_installed(package_name, version)

