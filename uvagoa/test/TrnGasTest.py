import unittest
import numpy as np
from uvagoa.test import UvagoaTest


class TrnGasTest(UvagoaTest):

    def calcObj1(self, atm, geo, wvln, squeeze):
        args = [wvln, geo.mu0, squeeze]
        trn1 = atm.trn_water(*args)
        trn2 = atm.trn_ozone(*args)
        trn3 = atm.trn_oxygen(*args)
        return trn1 * trn2 * trn3

    def testTrnGas_Atm0D_Geo0D_Val0D(self):
        obj0 = self.result["tdir_gas"]
        for squeeze in (False, True):
            shp1 = 3 * self.one(squeeze)
            obj1 = self.calcObj1(self.atm0, self.geo0, self.wvln[0], squeeze)
            flag = np.allclose(obj1, obj0[0], self.delta)
            self.assertTupleEqual(obj1.shape, shp1)
            self.assertTrue(flag)

    def testTrnGas_Atm0D_Geo0D_Val1D(self):
        shp0 = (self.wvln.size,)
        obj0 = self.result["tdir_gas"]
        for squeeze in (False, True):
            shp1 = 2 * self.one(squeeze) + shp0
            obj1 = self.calcObj1(self.atm0, self.geo0, self.wvln, squeeze)
            flag = np.allclose(obj1, obj0, self.delta)
            self.assertTupleEqual(obj1.shape, shp1)
            self.assertTrue(flag)

    def testTrnGas_Atm0D_Geo1D_Val0D(self):
        shp0 = (self.geo1.ngeo,)
        obj0 = self.result["tdir_gas"]
        for squeeze in (False, True):
            shp1 = self.one(squeeze) + shp0 + self.one(squeeze)
            obj1 = self.calcObj1(self.atm0, self.geo1, self.wvln[0], squeeze)
            idx1 = 0 if squeeze else (slice(None), 0)
            flag = np.allclose(obj1[idx1], obj0[0], self.delta)
            self.assertTupleEqual(obj1.shape, shp1)
            self.assertTrue(flag)

    def testTrnGas_Atm0D_Geo1D_Val1D(self):
        shp0 = (self.geo1.ngeo, self.wvln.size)
        obj0 = self.result["tdir_gas"]
        for squeeze in (False, True):
            shp1 = self.one(squeeze) + shp0
            obj1 = self.calcObj1(self.atm0, self.geo1, self.wvln, squeeze)
            idx1 = 0 if squeeze else (slice(None), 0)
            flag = np.allclose(obj1[idx1], obj0, self.delta)
            self.assertTupleEqual(obj1.shape, shp1)
            self.assertTrue(flag)

    def testTrnGas_Atm1D_Geo0D_Val1D(self):
        shp0 = (self.atm1.nscen, self.wvln.size)
        obj0 = self.result["tdir_gas"]
        for squeeze in (False, True):
            shp1 = shp0[:1] + self.one(squeeze) + shp0[1:]
            obj1 = self.calcObj1(self.atm1, self.geo0, self.wvln, squeeze)
            flag = np.allclose(obj1[0, :], obj0, self.delta)
            self.assertTupleEqual(obj1.shape, shp1)
            self.assertTrue(flag)

    def testTrnGas_Atm1D_Geo1D_Val0D(self):
        shp0 = (self.atm1.nscen, self.geo1.ngeo)
        obj0 = self.result["tdir_gas"]
        for squeeze in (False, True):
            shp1 = shp0 + self.one(squeeze)
            obj1 = self.calcObj1(self.atm1, self.geo1, self.wvln[0], squeeze)
            args = [self.wvln[0], self.geo1.mu0, squeeze]
            flag = np.allclose(obj1[0, 0], obj0[0], self.delta)
            self.assertTupleEqual(obj1.shape, shp1)
            self.assertTrue(flag)

    def testTrnGas_Atm1D_Geo1D_Val1D(self):
        shp0 = (self.atm1.nscen, self.geo1.ngeo, self.wvln.size)
        obj0 = self.result["tdir_gas"]
        for squeeze in (False, True):
            shp1 = shp0
            obj1 = self.calcObj1(self.atm1, self.geo1, self.wvln, squeeze)
            flag = np.allclose(obj1[0, 0], obj0, self.delta)
            self.assertTupleEqual(obj1.shape, shp1)
            self.assertTrue(flag)

if __name__ == "__main__":
    unittest.main()

