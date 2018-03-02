#!/usr/bin/python

import argparse
import libpacloud

def main():
    parser = argparse.ArgumentParser()
    package_group = parser.add_mutually_exclusive_group()
    package_group.add_argument('-s', '--search', help='search for specified package', metavar='package')
    package_group.add_argument('-i', '--install', help='install specified package', metavar='package')
    package_group.add_argument('-r', '--remove', help='remove specified package', metavar='package')
    package_group.add_argument('-c', '--compile', help='compile specified package', metavar='package')
    parser.add_argument('-u', '--update', help='update local database', action='store_true')
    parser.add_argument('-U', '--upgrade', help='upgrade system', action='store_true')
    parser.add_argument('--update-config', help='send user configuration to the server', action='store_true')

    args = parser.parse_args()
    args_dict = dict((k,v) for k,v in args.__dict__.items() if v is not None and v is not False)
    for (name, arg) in args_dict.items():
        func = getattr(libpacloud, name)
        func()

