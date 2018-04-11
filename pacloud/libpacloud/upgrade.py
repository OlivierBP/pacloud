#!/bin/python3

import libpacloud.database as db
from libpacloud.install import install

def upgrade():
  list = db.list_packages()
  list_dep = []
  for package in list:
    if (db.installed_version(package) != None):
      list_dep.extend(db.list_dependencies(package))
      install(package)
  return list_dep
