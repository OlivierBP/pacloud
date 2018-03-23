#!/usr/bin/python

import urllib.request

from libpacloud.config import SERVER_URL, DB_DIR

def get_package_url(package_name, version):
    return urllib.request.urlopen('{}/package/{}-{}'.format(SERVER_URL, package_name, version)).read().decode("utf-8")

def download_package(package_name, version):
    url = get_package_url(package_name, version)
    urllib.request.urlretrieve(url, '{}/{}/{}-{}.tbz2'.format(DB_DIR, package_name, package_name, version))

def download_db():
    return urllib.request.urlopen('{}/database/'.format(SERVER_URL)).read()

if __name__ == "__main__":
    download_package("example", "2.4")

