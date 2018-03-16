#!/usr/bin/python

import os
import json

def list_packages():
    packages = os.listdir('/var/lib/pacloud/db/')
    return packages

def info_package(pkg):
    data = json.load(open('/var/lib/pacloud/db/{}/metadata.json'.format(pkg)))
    return data

