from __future__ import division
from __future__ import print_function
import os.path
import unittest
import numpy as np
from uvagoa.api import Geometry
from uvagoa.api import Atmosphere


UNITTEST_FOLDER = os.path.dirname(__file__)


class UvagoaTest(unittest.TestCase):

    def one(self, squeeze):
        return () if squeeze else (1,)

    def setUp(self):
        """Set up the attributes needed for the test."""

        self.delta = 5E-4

        # Read the file with reference data.
        path = os.path.join(UNITTEST_FOLDER, "dat", "transmittance.dat")
        data = np.loadtxt(path).T

        # Extract the set of wavelengths in nanometers and microns.
        self.wvln = data[0]
        self.wvln_um = self.wvln / 1000.

        # Create the instances of Geometry, Atmosphere and define the albedo.
        self.geo0 = Geometry(lat=28.31, lon=-16.50, sza=60, day=152)
        self.atm0 = Atmosphere(p=800, o3=300, h2o=0.4, a=1.5, b=0.05)
        self.alb0 = 0.2

        # Create vectorised instances of Geometry, Atmosphere and albedo.
        self.geo1 = Geometry(
            lat=np.asarray([np.degrees(self.geo0.lat), 35.45]),
            lon=np.asarray([np.degrees(self.geo0.lon), 25.80]),
            sza=np.asarray([np.degrees(self.geo0.sza), 15.5]),
            day=np.asarray([self.geo0.day, 12]))
        self.atm1 = Atmosphere(
            p=np.asarray([self.atm0.p, 875.4, 925.3]),
            o3=np.asarray([self.atm0.o3, 286., 310]),
            h2o=np.asarray([self.atm0.h2o, 0.15, 0.01]),
            a=np.asarray([self.atm0.a, 0.75, 0.9]),
            b=np.asarray([self.atm0.b, 0.10, 0.15]))
        self.alb1 = np.asarray([self.alb0, 0.35, 0.7])

        # Store the results corresponding to the created instances.
        self.result = {
            "tau_ray": data[1],
            "tau_aer": data[2],
            "tdir_gas": data[4],
            "tdir_mix": data[5],
            "tglb_mix": data[6],
            "tdif_mix": data[7],
        }

    def tearDown(self):
        """Clean the attributes needed for the tests."""

        self.wvln = None
        self.wvln_um = None
        self.geo0 = None
        self.atm0 = None
        self.alb0 = None
        self.geo1 = None
        self.atm1 = None
        self.alb1 = None
        self.result = None


if __name__ == "__main__":

    import sys
    import glob
    import subprocess

    python_exec = "python{}".format(3 if sys.hexversion >= 0x03000000 else "")

    pattern = os.path.join(UNITTEST_FOLDER, "*.py")
    for path in glob.glob(pattern):
        if "__init__" not in path:
            print(os.path.basename(path))
            subprocess.call([python_exec, path])

