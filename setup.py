#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The setup script """

from setuptools import setup, find_packages
from htrest import __version__


# Get the description from the README file
with open('README.rst') as readme_file:
    readme = readme_file.read()

# Get the history from the HISTORY file
with open('HISTORY.rst') as history_file:
    history = history_file.read()


requirements = [
    'htheatpump==1.1.0',
    'flask==1.0.2',
    'flask_restplus==0.9.2',
    # put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # put package test requirements here
]


setup(
    # Project name
    name='htrest',

    # Versions should comply with PEP440. For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    # Project description
    description='Heliotherm heat pump REST API',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',

    # Choosen license
    license='GNU General Public License v3',

    # The project's main homepage
    url='https://github.com/dstrigl/HtREST',

    # Author details
    author='Daniel Strigl',
    #author_email='?',

    # Supported platforms
    platforms=['Linux'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(include=['htrest']),
    include_package_data=True,

    # Specification what the project minimally needs to run correctly, used by
    # pip to install its dependencies.
    install_requires=requirements,

    # prevent zip archive creation
    zip_safe=False,

    # keywords that describes the project
    keywords='python python3 heatpump Heliotherm rest restful api flask swagger',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Manufacturing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        # Language and Platform
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',

        # Additional topic classifier
        'Topic :: Communications',
        'Topic :: Home Automation',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Scientific/Engineering',
        'Topic :: Terminals :: Serial',
    ],

    # Test suite
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,

    # Entry points specification
    entry_points={
        'console_scripts': [
            'htrest=app:main',
        ]
    },
)
