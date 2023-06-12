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

from distutils.cmd import Command
try:
    from setuptools import setup
    install_requires = {"install_requires": "numpy"}
except ImportError:
    from distutils.core import setup 
    install_requires = {}


class UnittestCommand(Command):
    """Custom command to run the unit tests from the library."""

    description = "run unit tests from the library"
    user_options = []

    def initialize_options(self):
        import sys
        import os.path

        name = "__init__.py"
        fold = os.path.join(os.path.dirname(__file__), "solo", "test")
        path = os.path.join(fold, name)

        version = "{}".format(3 if sys.hexversion >= 0x03000000 else "")
        python_exec = "python{}".format(version)
        self.cmdlist = [python_exec, path]

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        subprocess.check_call(self.cmdlist)


kwargs = {
    "name":
        "solo",
    "version":
        "1.0.0+dev",
    "license":
        "GNU General Public License v2 or later (GPLv2+)",
    "description":
        "Python implementation of UVa-GOA radiative transfer model",
    "author":
        "Victor Molina Garcia",
    "author_email":
        "victor@goa.uva.es",
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
    "cmdclass": {
        "test": UnittestCommand,
    },
}

kwargs.update(install_requires)
setup(**kwargs)

