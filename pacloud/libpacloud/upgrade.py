#!/bin/python3

import libpacloud.database as db
from libpacloud.install import install

def update_all(package_name):
  list = db.list_packages()
  version = db.installed_version(package_name)
  for package in list:
    if version != None
      install(package_name)
      return list
