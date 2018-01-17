#! /usr/bin/env python3

try:
    from setuptools import setup
    install_requires = {"install_requires": "numpy"}
except ImportError:
    from distutils.core import setup 
    install_requires = {}

kwargs = {
    "name":
        "Solo",
    "version":
        "0.3",
    "license":
        "GPL-3.0",
    "description":
        "Python implementation of UVa-GOA radiative transfer model",
    "author":
        "Victoria E. Cachorro Revilla",
    "author_email":
        "chiqui@goa.uva.es",
    "maintainer":
        "Victor Molina Garcia",
    "maintainer_email":
        "victor@goa.uva.es",
    "url":
        "https://bitbucket.org/molinav/solo",
    "packages": [
        "solo",
        "solo.api",
        "solo.test",
    ],
    "package_data": {
        "solo": [
            "dat/*.dat",
            "test/dat/*.dat",
            "test/obj/atm/*.dat",
            "test/obj/geo/*.dat",
        ]
    },
}
kwargs.update(install_requires)
setup(**kwargs)

