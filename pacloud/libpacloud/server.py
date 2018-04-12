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

def _get_package_url(package_name, version):
    params = urllib.parse.urlencode({'package': package_name, 'version': version, 'useflag': urllib.parse.quote(USE)})
    res = urllib.request.urlopen('{}/LATEST/package?{}'.format(SERVER_URL, params)).read().decode('utf-8')
    return res

def download_package(package_name, version):
    url = _get_package_url(package_name, version)
    urllib.request.urlretrieve(url, '{}/{}/{}-{}.tbz2'.format(DB_DIR, package_name, package_name, version))

@errorsCatcher
def download_db():
    return urllib.request.urlopen('{}/database/'.format(SERVER_URL)).read().decode('utf-8')

def download_category(url):
    return urllib.request.urlopen(url).read().decode('utf-8')
