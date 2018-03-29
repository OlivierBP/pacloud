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
    package_group.add_argument('-q', '--query', help='return detailed informations regarding specified package', metavar='package')
    parser.add_argument('-u', '--update', help='update local database', action='store_true')
    parser.add_argument('-U', '--upgrade', help='upgrade system', action='store_true')
    parser.add_argument('--update-config', help='send user configuration to the server', action='store_true')

    args = parser.parse_args()
    args_dict = dict((k,v) for k,v in args.__dict__.items() if v is not None and v is not False)
    for (name, arg) in args_dict.items():
        if name == "search":
            search(arg)
        elif name == "update":
            update()
        elif name == "install":
            install(arg)
        elif name == "remove":
            remove(arg)
        elif name == "query":
            query(arg)
        else:
            func = getattr(libpacloud, name)
            if (arg):
                print(func(arg))
            else:
                func()

def search(arg):
    results = libpacloud.search(arg)
    if not results:
        print("No result found for search key: {}".format(arg))
        return
    print("Results for search key: {}".format(arg))
    for package in results:
        firstline = "\n\033[1m{}\033[0;36m (".format(package['name'])
        for version in package['versions']:
            firstline += " {} ".format(version['number'])
        firstline += ")\033[0m "
        try:
            firstline += "\033[32m[installed: {}]\033[0m".format(package['installed'])
        except KeyError:
            pass
        print(firstline)
        print("\t"+package["description"])

def update():
    print('Update...')
    libpacloud.update()
    print('Done!')

def install(arg):
    version = None
    if('-' in arg):
        version = arg[arg.find('-')+1:]
        arg = arg[:arg.find('-'):]
    print("Resolving dependencies...\n")
    dependencies_list = libpacloud.list_dependencies(arg, version)
    strdep = "Packages ({}):".format(len(dependencies_list))
    for dependency in dependencies_list:
        strdep += " {} ".format(dependency)
    print(strdep +"\n")
    if(_yesno("Do you want to proceed with installation? [Y/n] ")):
        print("Installing packages...")
        for package in dependencies_list:
            print(package + "... ", end="")
            libpacloud.install(package, version)
            version = None
            print("done!")
        print("Done!")

def remove(arg):
    print('Resolving dependencies...\n')
    dependencies_list = libpacloud.list_remove_dependencies(arg)
    strdep = "Packages ({}):".format(len(dependencies_list))
    for dependency in dependencies_list:
        strdep += " {} ".format(dependency)
    print(strdep +"\n")
    if(_yesno("Do you want to remove these packages? [Y/n] ")):
        for package in dependencies_list:
            print(package + "... ", end="")
            libpacloud.remove(arg)
            print("done!")
        print("Done!")

def query(arg):
    results = libpacloud.search(arg)
    if(len(results) != 1):
        print('Ambiguous search. Aborting.')
        return
    print('Name        : {}'.format(results[0]['name']))
    print('Description : {}'.format(results[0]['description']))
    print('Versions    :')
    for version in results[0]['versions']:
        print('  - Number  : {}'.format(version['number']))
        print('    Dependencies:', end="")
        for dep in version['dependencies']:
            print(' {} '.format(dep), end="")
        print()
    try:
        print('Installed   : {}'.format(results[0]['installed']))
    except KeyError:
        pass
    try:
        results[0]['required_by']
        print('Required by :', end="")
        for req in results[0]['required_by']:
            print(' {} '.format(req), end="")
        print()
    except KeyError:
        pass

def _yesno(message):
    user_choice = input(message)
    return user_choice in ['', 'Y', 'y']

