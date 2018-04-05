#!/bin/python3

import libpacloud.database as db
from libpacloud.install import install

def update_all():
  list = db.list_packages()
  for package in list:
    return list
    install()
