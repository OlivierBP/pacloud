#!/usr/bin/python

import urllib.request

from config import SERVER_URL, DB_DIR

def get_package_url(package_name, version):
    return urllib.request.urlopen('{}/packages/{}-{}'.format(SERVER_URL, package_name, version)).read().decode("utf-8")

def download_package(package_name, version):
    url = get_package_url(package_name, version)
    urllib.request.urlretrieve(url, '{}/{}/{}-{}.tar.gz'.format(DB_DIR, package_name, version))

if __name__ == "__main__":
    download_package("example", "2.4")

