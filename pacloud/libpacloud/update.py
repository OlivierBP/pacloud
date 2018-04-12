#!/usr/bin/python

import json

from libpacloud.server import download_db, download_category
import libpacloud.database as db

def update():
    packages = db.list_packages()
    for line in download_db().splitlines():
        print(line, end="")
        try:
            new_db = json.loads(download_category(line), strict=False)
        except json.decoder.JSONDecodeError:
            print(' failed!')
            continue
        print(' downloaded')
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
