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
"""Basic tests for the :class:`Geometry` class."""

import os.path
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import numpy as np
from solo.api import Geometry


class TestGeometry(unittest.TestCase):
    """Basic tests for the :class:`Geometry` class."""

    @staticmethod
    def get_geometry_filepath(name):
        """Return path to a :class:`Geometry` test file."""

        here = os.path.dirname(__file__)
        geodir = os.path.join(here, "obj", "geo")
        return os.path.join(geodir, name)

    def _test_load(self, name, expected):
        """Test loading of a :class:`Geometry` file."""

        geo = Geometry.from_file(self.get_geometry_filepath(name))
        self.assertEqual(geo, expected)

    def test_load_geo11(self):
        """Test loading of a :class:`Geometry` file."""

        expected = Geometry(
            day=152, sec=None, lat=None, lon=None, sza=60, mode="deg")
        self._test_load("geo11.dat", expected)

    def test_load_geo12(self):
        """Test loading of a :class:`Geometry` file."""

        expected = Geometry(
            day=152, sec=25311, lat=0.49410271, lon=-0.28797933,
            sza=1.39777933, mode="rad")
        self._test_load("geo12.dat", expected)

    def test_load_geo13(self):
        """Test loading of a :class:`Geometry` file."""

        expected = Geometry(
            day=152, sec=43510, lat=0.49410271, lon=-0.28797933,
            sza=0.2546518, mode="rad")
        self._test_load("geo13.dat", expected)

    def test_load_geo21(self):
        """Test loading of a :class:`Geometry` file."""

        expected = Geometry(
            day=np.array([152, 152, 152, 152, 153]), sec=None, lat=None,
            lon=None, sza=np.array([60, 50.4, 15.1, 21, 75.]), mode="deg")
        self._test_load("geo21.dat", expected)

    def test_load_geo22(self):
        """Test loading of a :class:`Geometry` file."""

        expected = Geometry(
            day=np.array([152, 180, 235]),
            sec=np.array([25311, 5678, 47162]),
            lat=np.array([0.49410271, 0.83950337, 0.00872665]),
            lon=np.array([-0.28797933, 1.31772359, 0.6981317]),
            sza=np.array([1.39777933, 1.17809272, 0.98533964]),
            mode="rad")
        self._test_load("geo22.dat", expected)

    def test_load_geo23(self):
        """Test loading of a :class:`Geometry` file."""

        expected = Geometry(
            day=np.array([152, 180, 235]),
            sec=np.array([43510, 47175, 50820]),
            lat=np.array([0.49410271, 0.83950337, 0.00872665]),
            lon=np.array([-0.28797933, 1.31772359, 0.6981317]),
            sza=np.array([0.2546518, 1.28671359, 1.24504354]),
            mode="rad")
        self._test_load("geo23.dat", expected)


if __name__ == "__main__":
    unittest.main()
