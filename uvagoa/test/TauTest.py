import unittest
import numpy as np
from uvagoa.test import UvagoaTest


class TauTest(UvagoaTest):

    def testTauRayleigh_Atm0D_Val0D_Squeeze0(self):
        shp0 = (1, 1)
        obj0 = self.result["tau_ray"]
        obj1 = self.atm0.tau_rayleigh(self.wvln_um[0], squeeze=False)
        flag = np.allclose(obj1, obj0[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)

    def testTauRayleigh_Atm0D_Val0D_Squeeze1(self):
        shp0 = ()
        obj0 = self.result["tau_ray"]
        obj1 = self.atm0.tau_rayleigh(self.wvln_um[0], squeeze=True)
        flag = np.allclose(obj1, obj0[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)

    def testTauRayleigh_Atm1D_Val0D_Squeeze0(self):
        shp0 = (self.atm1.nscen, 1)
        obj0 = self.result["tau_ray"]
        obj1 = self.atm1.tau_rayleigh(self.wvln_um[0], squeeze=False)
        flag = np.allclose(obj0[0], obj1[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)

    def testTauRayleigh_Atm1D_Val0D_Squeeze1(self):
        shp0 = (self.atm1.nscen,)
        obj0 = self.result["tau_ray"]
        obj1 = self.atm1.tau_rayleigh(self.wvln_um[0], squeeze=True)
        flag = np.allclose(obj1[0], obj0[0], self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)

    def testTauRayleigh_Atm0D_Val1D_Squeeze0(self):
        shp0 = (1, self.wvln_um.size)
        obj0 = self.result["tau_ray"]
        obj1 = self.atm0.tau_rayleigh(self.wvln_um, squeeze=False)
        flag = np.allclose(obj0, obj1, self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)

    def testTauRayleigh_Atm0D_Val1D_Squeeze1(self):
        shp0 = (self.wvln_um.size,)
        obj0 = self.result["tau_ray"]
        obj1 = self.atm0.tau_rayleigh(self.wvln_um, squeeze=True)
        flag = np.allclose(obj1, obj0, self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)

    def testTauRayleigh_Atm1D_Val1D_Squeeze0(self):
        shp0 = (self.atm1.nscen, self.wvln_um.size,)
        obj0 = self.result["tau_ray"]
        obj1 = self.atm1.tau_rayleigh(self.wvln_um, squeeze=False)
        flag = np.allclose(obj1[0], obj0, self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)

    def testTauRayleigh_Atm1D_Val1D_Squeeze1(self):
        shp0 = (self.atm1.nscen, self.wvln_um.size,)
        obj0 = self.result["tau_ray"]
        obj1 = self.atm1.tau_rayleigh(self.wvln_um, squeeze=True)
        flag = np.allclose(obj1[0], obj0, self.delta)
        self.assertTupleEqual(obj1.shape, shp0)
        self.assertTrue(flag)


if __name__ == "__main__":
    unittest.main()

