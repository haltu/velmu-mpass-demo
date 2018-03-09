#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = open('README.rst').read()

def get_version():
    try:
        import subprocess
        p = subprocess.Popen('hg id -t', shell=True, stdout=subprocess.PIPE)
        tag = p.stdout.read()[1:].strip()
        return tag
    except:
        return 'dev'

setup(
    name='mpass',
    version=get_version(),
    description="""MPASS""",
    long_description=readme,
    author='Haltu',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-parler',
        'requests',
    ],
    license="Modified BSD",
    zip_safe=False,
    keywords='mpass',
)
