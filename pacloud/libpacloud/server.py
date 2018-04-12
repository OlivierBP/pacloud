#!/usr/bin/python

import urllib.request
import urllib.parse
import json
import time

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
    res = json.loads(_download('{}/LATEST/package?{}'.format(SERVER_URL, params)))
    return res

def download_package(package_name, version):
    response_json = _get_package_url(package_name, version)
    if(response_json["status"] == "SUCCESS"):
        print(response_json["linkS3"])
        urllib.request.urlretrieve(response_json["linkS3"], '{}/{}/{}-{}.tbz2'.format(DB_DIR, package_name, package_name[package_name.find('/')+1:], version))
    elif(response_json["status"] == "WAIT"):
        print('.', end="")
        time.sleep(10)
        download_package(package_name, version)
        #raise Exception("WAIT")
    else:
        raise Exception(response_json["errorMessage"])

@errorsCatcher
def download_db():
    return _download('{}/database/'.format(SERVER_URL))

def download_category(url):
    return _download(url)
