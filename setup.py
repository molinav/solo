#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, 2023 Víctor Molina García
#
# This file is part of solo.
#
# solo is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# solo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with solo; if not, see <https://www.gnu.org/licenses/>.
#
"""solo -- Core of the SSolar-GOA radiative transfer library."""

import io
import os
import re
import sys
from setuptools import setup
from setuptools import find_packages


def get_content(name, splitlines=False):
    """Return the file contents with project root as root folder."""

    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, name)
    with io.open(path, "r", encoding="utf-8") as fd:
        content = fd.read()
    if splitlines:
        content = [row for row in content.splitlines() if row]
    return content


def get_version(pkgname):
    """Return package version without importing the file."""

    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, "src", pkgname, "__init__.py")
    with io.open(path, "r", encoding="utf-8") as fd:
        pattern = r"""\n__version__[ ]*=[ ]*["']([^"]+)["']"""
        return re.search(pattern, fd.read()).group(1)


install_requires = get_content("requirements.txt", splitlines=True)
if sys.version_info[:2] == (3, 2):
    # Hack for Python 3.2 because pip < 8 cannot handle version markers.
    marker = '; python_version == "3.2"'
    install_requires = [
        item.replace(marker, "") for item in install_requires
        if item.endswith(marker)]

setup(**{
    "name":
        "solo",
    "version":
        "1.0.0+dev",
    "license":
        "GNU General Public License v2 or later (GPLv2+)",
    "description":
        "Core of the SSolar-GOA radiative transfer library",
    "long_description":
        get_content("README.md"),
    "long_description_content_type":
        "text/markdown",
    "url":
        "https://bitbucket.org/molinav/solo",
    "author":
        "Víctor Molina García",
    "author_email":
        "victor@goa.uva.es",
    "maintainer":
        "Víctor Molina García",
    "maintainer_email":
        "victor@goa.uva.es",
    "package_dir":
        {"": "src"},
    "packages":
        find_packages(where="src"),
    "package_data": {
        "solo": [
            "dat/*.dat",
            "test/dat/*.dat",
            "test/obj/atm/*.dat",
            "test/obj/geo/*.dat",
        ]
    },
    "install_requires":
        install_requires,
})
