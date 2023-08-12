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

    def test_init_error_size_mismatch(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sza=np.array([45, 60]), mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_ndim(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=np.array([[1]]), sza=np.array([[45]]), mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_mode(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sza=45, mode="foo")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_julian_day_too_low(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=0, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_julian_day_too_big(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=367, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_sec_too_low(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sza=-0.01, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_sec_too_big(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sec=-1, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_lat_too_low(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, lat=-90.1, lon=0.0, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_lat_too_big(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, lat=+90.1, lon=0.0, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_lon_too_low(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, lat=0.0, lon=-180.1, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_lon_too_big(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, lat=0.0, lon=+180.1, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_sza_too_low(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sec=86400, sza=45, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_invalid_sza_too_big(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sza=180.01, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_sza_none_and_missing_sec(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sec=None, lat=45.0, lon=20.0, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_sza_none_and_missing_lat(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sec=0, lat=None, lon=20.0, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_error_sza_none_and_missing_lon(self):
        """Test :class:`Geometry` creation error due to wrong inputs."""

        kwds = dict(day=1, sec=0, lat=45.0, lon=None, mode="deg")
        self.assertRaises(ValueError, Geometry, **kwds)

    def test_init_with_mode_deg(self):
        """Test successful :class:`Geometry` creation."""

        geo = Geometry(day=1, sec=0, sza=45, mode="deg")
        self.assertIsInstance(geo, Geometry)
        self.assertEqual(geo, geo)

    def test_init_with_mode_rad(self):
        """Test successful :class:`Geometry` creation."""

        geo = Geometry(day=1, sec=0, sza=0.5, mode="rad")
        self.assertIsInstance(geo, Geometry)
        self.assertEqual(geo, geo)

    def test_init_with_sza_from_location(self):
        """Test successful :class:`Geometry` creation."""

        geo = Geometry(day=1, sec=0, lat=0.0, lon=0.0, mode="deg")
        self.assertIsInstance(geo, Geometry)
        self.assertEqual(geo, geo)

    def test_ngeo_scalar(self):
        """Test `ngeo` property of :class:`Geometry` objects."""

        geo = Geometry(day=1, sza=45, mode="deg")
        self.assertEqual(geo.ngeo, 1)

    def test_ngeo_vector_size_1(self):
        """Test `ngeo` property of :class:`Geometry` objects."""

        geo = Geometry(day=np.array([1]), sza=np.array([0]), mode="deg")
        self.assertEqual(geo.ngeo, 1)

    def test_ngeo_vector_size_2(self):
        """Test `ngeo` property of :class:`Geometry` objects."""

        geo = Geometry(day=np.array([1, 2]), sza=np.array([0, 45]), mode="deg")
        self.assertEqual(geo.ngeo, 2)

    def test_day_angle_scalar_001(self):
        """Test `day_angle` property of :class:`Geometry` objects."""

        geo = Geometry(day=1, sza=45, mode="deg")
        self.assertEqual(geo.day_angle, 0)

    def test_day_angle_scalar_366(self):
        """Test `day_angle` property of :class:`Geometry` objects."""

        geo = Geometry(day=366, sza=45, mode="deg")
        self.assertEqual(geo.day_angle, 2 * np.pi)

    def test_eq_true(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sza=45)
        geo2 = Geometry(day=1, sza=45)
        self.assertEqual(geo1, geo2)

    def test_eq_false_different_types(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sza=45)
        geo2 = None
        self.assertNotEqual(geo1, geo2)

    def test_eq_false_different_sizes(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sza=45)
        geo2 = Geometry(day=np.array([1, 1]), sza=np.array([45, 45]))
        self.assertNotEqual(geo1, geo2)

    def test_eq_false_different_days(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sza=45)
        geo2 = Geometry(day=2, sza=45)
        self.assertNotEqual(geo1, geo2)

    def test_eq_false_different_secs(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sec=0, sza=45)
        geo2 = Geometry(day=1, sec=1, sza=45)
        self.assertNotEqual(geo1, geo2)

    def test_eq_false_different_szas(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sza=45)
        geo2 = Geometry(day=1, sza=46)
        self.assertNotEqual(geo1, geo2)

    def test_eq_false_different_lats(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sec=0, lat=45.0, lon=20.0)
        geo2 = Geometry(day=1, sec=0, lat=46.0, lon=20.0)
        self.assertNotEqual(geo1, geo2)

    def test_eq_false_different_lons(self):
        """Test :class`Geometry` equality operator."""

        geo1 = Geometry(day=1, sec=0, lat=45.0, lon=20.0)
        geo2 = Geometry(day=1, sec=0, lat=45.0, lon=21.0)
        self.assertNotEqual(geo1, geo2)

    def test_geometric_factor_scalar_001(self):
        """Test :meth:`Geometry.geometric_factor` method."""

        geo = Geometry(day=1, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.geometric_factor(), 1.035049))

    def test_geometric_factor_scalar_180(self):
        """Test :meth:`Geometry.geometric_factor` method."""

        geo = Geometry(day=180, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.geometric_factor(), 0.966734))

    def test_geometric_factor_scalar_366(self):
        """Test :meth:`Geometry.geometric_factor` method."""

        geo = Geometry(day=366, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.geometric_factor(), 1.035049))

    def test_declination_scalar_001(self):
        """Test :meth:`Geometry.declination` method."""

        geo = Geometry(day=1, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.declination(), -0.401065))

    def test_declination_scalar_180(self):
        """Test :meth:`Geometry.declination` method."""

        geo = Geometry(day=180, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.declination(), +0.405536))

    def test_declination_scalar_366(self):
        """Test :meth:`Geometry.declination` method."""

        geo = Geometry(day=366, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.declination(), -0.401065))

    def test_equation_of_time_scalar_001(self):
        """Test :meth:`Geometry.equation_of_time` method."""

        geo = Geometry(day=1, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.equation_of_time(), -0.0146219))

    def test_equation_of_time_scalar_180(self):
        """Test :meth:`Geometry.equation_of_time` method."""

        geo = Geometry(day=180, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.equation_of_time(), -0.0142206))

    def test_equation_of_time_scalar_366(self):
        """Test :meth:`Geometry.equation_of_time` method."""

        geo = Geometry(day=366, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.equation_of_time(), -0.0146219))

    def test_compute_sza(self):
        """Test :meth:`Geometry.compute_sza` method for existing instance."""

        geo = Geometry(day=1, sza=45, mode="deg")
        self.assertTrue(np.allclose(geo.compute_sza(), geo.sza))

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
