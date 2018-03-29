#!/usr/bin/python

import libpacloud.database as db
import libpacloud.packages as pkg

def list_remove_dependencies(package_name):
    dependencies = pkg.list_dependencies(package_name)
    for dep in dependencies:
        try:
            if(len(db.info_package(dep)["required_by"]) > 1):
                dependencies.remove(dep)
        except KeyError:
            pass
    return dependencies

def remove(package_name):
    pkg.remove(package_name)
    db.mark_as_uninstalled(package_name)
