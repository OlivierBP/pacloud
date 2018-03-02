#!/usr/bin/python
#-*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='pacloud',
    version='0.0.1',
    description='package manager building your packages on the Cloud',
    author='Olivier Bal-Pétré, Juliette Faro, Pierre Varlez',
    python_requires='>=3.6.0',
    url='https://github.com/OlivierBP/pacloud',
    license='MIT',
    
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        pacloud=pacloud.main:main
    '''
)

