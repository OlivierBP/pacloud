#!/usr/bin/python

import urllib.request
import urllib.parse

from libpacloud.config import SERVER_URL, DB_DIR, USE

def errorsCatcher(f):
    def new_f():
        try:
            return f()
        except urllib.error.HTTPError:
            print("An HTTP error occured")
    return new_f

def _download(url):
    return urllib.request.urlopen(url).read().decode('utf-8')

def _get_package_url(package_name, version):
    params = urllib.parse.urlencode({'package': package_name, 'version': version, 'useflag': urllib.parse.quote(USE)})
    res = _download('{}/LATEST/package?{}'.format(SERVER_URL, params))
    return res

def download_package(package_name, version):
    url = _get_package_url(package_name, version)
    urllib.request.urlretrieve(url, '{}/{}/{}-{}.tbz2'.format(DB_DIR, package_name, package_name, version))

@errorsCatcher
def download_db():
    return _download('{}/database/'.format(SERVER_URL))

def download_category(url):
    return _download(url)
