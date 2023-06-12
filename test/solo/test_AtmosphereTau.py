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

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import numpy as np
from . import TestSolo


class TestAtmosphereTau(TestSolo):

    def testTauRayleigh_Atm0D_Val0D(self):
        shp0 = ()
        obj0 = self.result["tau_ray"]
        shp1 = 2 * self.one() + shp0
        obj1 = self.atm0.tau_rayleigh(self.wvln_um[0])
        flag = np.allclose(obj1, obj0[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)

    def testTauRayleigh_Atm0D_Val1D(self):
        shp0 = (self.wvln_um.size,)
        obj0 = self.result["tau_ray"]
        shp1 = self.one() + shp0
        obj1 = self.atm0.tau_rayleigh(self.wvln_um)
        flag = np.allclose(obj1, obj0, self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)

    def testTauRayleigh_Atm1D_Val0D(self):
        shp0 = (self.atm1.nscen,)
        obj0 = self.result["tau_ray"]
        shp1 = shp0 + self.one()
        obj1 = self.atm1.tau_rayleigh(self.wvln_um[0])
        flag = np.allclose(obj1[0], obj0[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)

    def testTauRayleigh_Atm1D_Val1D(self):
        shp0 = (self.atm1.nscen, self.wvln_um.size,)
        obj0 = self.result["tau_ray"]
        shp1 = shp0
        obj1 = self.atm1.tau_rayleigh(self.wvln_um)
        flag = np.allclose(obj1[0], obj0, self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)

    def testTauAerosols_Atm0D_Val0D(self):
        shp0 = ()
        obj0 = self.result["tau_aer"]
        shp1 = 2 * self.one() + shp0
        obj1 = self.atm0.tau_aerosols(self.wvln_um[0])
        flag = np.allclose(obj1, obj0[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)

    def testTauAerosols_Atm0D_Val1D(self):
        shp0 = (self.wvln_um.size,)
        obj0 = self.result["tau_aer"]
        shp1 = self.one() + shp0
        obj1 = self.atm0.tau_aerosols(self.wvln_um)
        flag = np.allclose(obj1, obj0, self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)

    def testTauAerosols_Atm1D_Val0D(self):
        shp0 = (self.atm1.nscen,)
        obj0 = self.result["tau_aer"]
        shp1 = shp0 + self.one()
        obj1 = self.atm1.tau_aerosols(self.wvln_um[0])
        flag = np.allclose(obj1[0], obj0[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)

    def testTauAerosols_Atm1D_Val1D(self):
        shp0 = (self.atm1.nscen, self.wvln_um.size,)
        obj0 = self.result["tau_aer"]
        shp1 = shp0
        obj1 = self.atm1.tau_aerosols(self.wvln_um)
        flag = np.allclose(obj1[0], obj0, self.delta)
        self.assertTupleEqual(obj1.shape, shp1)
        self.assertTrue(flag)


if __name__ == "__main__":
    unittest.main()
