#!/usr/bin/python

import json

from libpacloud.server import download_db
import libpacloud.database as db

def update():
    new_db = json.loads(download_db())
    packages = db.list_packages()
    # Adding new packages and modifying existing ones
    for package in new_db:
        if(package["name"] in packages):
            db.modify_package(package["name"], package)
            packages.remove(package["name"])
        else:
            db.add_package(package["name"], package)
    # Removing packages that are in the local database but not in the server one
    for package in packages:
        db.remove_package(package)
