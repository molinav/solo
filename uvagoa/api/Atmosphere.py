from __future__ import division
from collections import namedtuple
import os.path
import numpy as np


ATTRS = ["p", "o3", "h2o", "a", "b", "w0", "g"]

# Define the default values for optional atmospheric input arguments.
DEFAULT_W0 = 0.90
DEFAULT_G = 0.85

# Load the array of molecular absorption coefficients in read-only mode.
DIRFOLD = os.path.dirname(os.path.abspath(__file__))
ABSCOEF_PATH = os.path.join(os.path.dirname(DIRFOLD), "dat", "abscoef.dat")
ABSCOEF = np.loadtxt(ABSCOEF_PATH, usecols=(0, 1, 2, 3, 4)).T
ABSCOEF.flags.writeable = False


class Atmosphere(namedtuple("Atmosphere", ATTRS)):
    """Class to define the geometric properties of the atmospheric view.

    Every instance allows the access to the following properties:

        nscen : int
            number of scenarios

        p : array-like, (nscen,)
            atmospheric pressure at the viewing position in hPa

        o3 : array-like, (nscen,)
            vertical ozone content in DU

        h2o : array-like, (nscen,)
            total amount of water vapour in cm-pr

        a : array-like, (nscen,)
            Angstrom alpha parameter

        b : array-like, (nscen,)
            Angstrom beta parameter

        w0 : array-like, (nscen,)
            single scattering albedo

        g : array-like, (nscen,)
            aerosol asymmetry parameter
    """

    def __new__(cls, p, o3, h2o, a, b, w0=None, g=None):

        # Ensure that the input arguments have consistent shapes and sizes.
        items = [p, o3, h2o, a, b] + [x for x in [w0, g] if x is not None]
        set_shapes = set(np.shape(x) for x in items)
        if len(set_shapes) > 1:
            raise AttributeError("size mismatch among input arguments")
        set_shapes = list(set_shapes)[0]
        if len(set_shapes) > 1:
            raise AttributeError("input arguments must be 0- or 1-dimensional")

        # Ensure that the input arguments are within range and set the default
        # values for 'w0' and 'g' if they were not defined.
        if np.any(p < 0):
            raise ValueError("pressure out of range")
        if np.any(o3 < 0):
            raise ValueError("ozone out of range")
        if np.any(h2o < 0):
            raise ValueError("water vapour out of range")
        if np.any(a < 0):
            raise ValueError("Angstrom alpha out of range")
        if np.any(b < 0):
            raise ValueError("Angstrom beta out of range")
        if w0 is None:
            w0 = np.full(shape=set_shapes, fill_value=DEFAULT_W0, dtype=float)
        elif np.any(w0 < 0) or np.any(w0 > 1):
            raise ValueError("single scattering albedo out of range")
        if g is None:
            g = np.full(shape=set_shapes, fill_value=DEFAULT_G, dtype=float)
        elif np.any(np.abs(g) > 1):
            raise ValueError("asymmetry parameter out of range")

        # Return the new instance.
        atm = super(Atmosphere, cls).__new__(cls, p, o3, h2o, a, b, w0, g)
        return atm

    @property
    def nscen(self):
        """Return the number of scenarios stored within the instance."""

        shp = np.shape(self.p)
        return shp[0] if shp else 1

    @property
    def abscoef(self):
        """Return the molecular absorption coefficients.

        The first row stores the wavelengths in nm (from 300 to 2600 nm),
        while the other rows provide the absorption coefficients for the
        following constituents:

            1 : water vapour,
            2 : water vapour,
            3 : ozone,
            4 : molecular oxygen.

        Return:

            abscoef : array-like, shape (1 + ncoef, nwvln)
                absorption coefficients for different types of molecules
                as a function of the wavelength in nm, which is stored
                in the first row
        """

        return ABSCOEF

