#!/bin/python3

import server

list=[]

def check_dep(pkg):
    if len(pkg.dep == 0) and pkg not in list:
        list.append(pkg)
    else:
        for dep in pkg.dep:
            if pkg not in list:
                list.appen(pkg)
            if dep not in list:
                check.dep(dep)



if _name_ == '_main_':
    main()
