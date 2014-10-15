#!/usr/bin/env python
"""
schemadoc
==========

MySQL documentaiton generatiln tool.

$ schemadoc -h<host> -u<user> -p<password> -D<database>
"""

from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('schemadoc/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='schemadoc',
    version=main_ns['__version__'],
    author='Maksym Markov',
    author_email='maksym.markov@gmail.com',
    url='https://github.com/mmarkov/schema-doc',
    description='MySQL Database documentation generator',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    license='BSD',
    install_requires=[
        'jinja2',
        'PyMySQL',
        ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'schema-doc = schemadoc:main',
            ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    )
