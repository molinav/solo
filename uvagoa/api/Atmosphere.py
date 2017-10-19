from __future__ import division
from collections import namedtuple
import os.path
import numpy as np


ATTRS = ["p", "o3", "h2o", "a", "b", "w0", "g"]

# Define the default values for optional atmospheric input arguments.
DEFAULT_P = 1013.
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

        p : array-like, shape (nscen,)
            atmospheric pressure at the viewing position in hPa

        o3 : array-like, shape (nscen,)
            vertical ozone content in DU

        h2o : array-like, shape (nscen,)
            total amount of water vapour in cm-pr

        a : array-like, shape (nscen,)
            Angstrom alpha parameter

        b : array-like, shape (nscen,)
            Angstrom beta parameter

        w0 : array-like, shape (nscen,)
            single scattering albedo

        g : array-like, shape (nscen,)
            aerosol asymmetry parameter
    """

    def __new__(cls, p, o3, h2o, a, b, w0=None, g=None):
        """Return a new instance of Atmosphere.

        Receive:

            p : array-like, shape (nscen?,)
                atmospheric pressure at the viewing position in hPa
            o3 : array-like, shape (nscen?,)
                vertical ozone content in DU
            h2o : array-like, shape (nscen?,)
                total amount of water vapour in cm
            a : array-like, shape (nscen?,)
                Angstrom alpha parameter
            b : array-like, shape (nscen?,)
                Angstrom beta parameter
            w0 : array-like, shape (nscen?,)
                single scattering albedo, default given by DEFAULT_W0
            g : array-like, shape (nscen?,)
                aerosol asymmetry parameter, default given by DEFAULT_G

        Return:

            atm : Atmosphere
                instance of Atmosphere based on the input parameters

        Raise:

            AttributeError
                if input arguments have inconsistent or wrong shapes
            ValueError
                if the input arguments are out of range
        """

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

    def tau_rayleigh(self, wvln_um):
        """Return the Rayleigh optical depth for the given wavelengths.

        The optical depth is computed by using Bates's formula:

            tau_ray(wvln) = 1 / (117.2594 * (wvln / um)**4
                                 - 1.3215 * (wvln / um)**2 + 0.000320
                                 - 0.000076 * (wvln / um)**(-4)),

        which is obtained for a location with atmospheric pressure equal
        to 1 atm. For other pressures, the formula must be multiplied by
        the factor (pressure / 1013 hPa).

        Receive:

            wvln_um : array-like, shape (nwvln?,)
                wavelengths in microns

        Return:

            tau : array-like, shape (nscen?, nwvln?)
                Rayleigh optical depth for every scenario and wavelength

        Raise:

            ValueError
                if the input 'wvln_um' does not have a proper shape
        """

        # Ensure shape of input argument.
        if len(np.shape(wvln_um)) > 1:
            raise ValueError("'wvln_um' must be 0- or 1-dimensional")

        # Define the coefficients used in the formula.
        c = [117.2594, -1.3215, 0.000320, -0.000076]

        # Broadcast arrays before the computation of 'tau'.
        wvln_um = np.atleast_1d(wvln_um)
        pressure = np.atleast_1d(self.p)[:, None]

        # Compute the optical thickness using Bates' formula, which must be
        # corrected with the real pressure because the original formula is
        # only valid for an atmospheric pressure of 1 atm.
        div = c[0] * wvln_um**4 + c[1] * wvln_um**2 + c[2] + c[3] * wvln_um**-4
        tau = (pressure / DEFAULT_P) / div
        return np.squeeze(tau)

    def tau_aerosols(self, wvln_um):
        """Return the aerosol optical depth for the given wavelengths.

        The optical depth is computed by using the Angstrom's formula:

            tau_aer(wvln) = beta * (wvln / um)**(-alpha).

        Receive:

            wvln_um : array-like, shape (nwvln?,)
                wavelengths in microns

        Return:

            tau : array-like, shape (nscen?, nwvln?)
                aerosol optical depth for every scenario and wavelength

        Raise:

            ValueError
                if the input 'wvln_um' does not have a proper shape
        """

        # Ensure shape of input argument.
        if len(np.shape(wvln_um)) > 1:
            raise ValueError("'wvln_um' must be 0- or 1-dimensional")

        # Broadcast arrays before the computation of 'tau'.
        wvln_um = np.atleast_1d(wvln_um)
        alpha = np.atleast_1d(self.a)[:, None]
        beta = np.atleast_1d(self.b)[:, None]

        # Compute the optical thickness using Angstrom's formula.
        tau = beta * wvln_um**(-alpha)
        return np.squeeze(tau)

    def trn_ozone(self, wvln, mu0):
        """Return the transmittance due to ozone absorption.

        The transmittance is computed by using the formula:

            trn_o3(wvln) = np.exp(-kabs_o3(wvln) * path_o3 / mu0),

        where 'kabs_o3' denotes the ozone absorption coefficients
        in cm-1, 'path_o3' is the ozone absorption path given in cm
        and 'mu0' is the cosine of the solar zenith angle.

        Receive:

            wvln : array-like, shape (nwvln?,)
                wavelengths in nanometers
            mu0 : array-like, shape (ngeo?,)
                cosines of the solar zenith angle

        Return:

            trn : array-like, shape (nscen?, ngeo?, nwvln)
                ozone transmittance for every scenario, geometry and
                wavelength

        Raise:

            ValueError
                if the input 'wvln' does not have a proper shape
        """

        # Ensure shape of the input arguments.
        if len(np.shape(wvln)) > 1:
            raise ValueError("'wvln' must be 0- or 1-dimensional")
        if len(np.shape(mu0)) > 1:
            raise ValueError("'mu0' must be 0- or 1-dimensional")

        # Compute the absorption cross sections for ozone at the given input
        # wavelengths by using linear interpolation, and convert them to
        # absorption coefficients in cm-1 by using Loschmidt's number.
        ozone_xsec = np.atleast_1d(np.interp(wvln, *self.abscoef[[0, 3]]))
        ozone_coef = (2.687E19 * ozone_xsec)
        mu0 = np.atleast_1d(mu0)[:, None]

        # Convert from ozone amount in DU to ozone absorption path in cm.
        ozone_path = np.atleast_1d(1E-3 * self.o3)[:, None, None]

        trn = np.exp(-ozone_coef * ozone_path / mu0)
        return np.squeeze(trn)

    def trn_oxygen(self, wvln, mu0):
        """Return the transmittance due to molecular oxygen absorption.

        The transmittance is computed by using the formula:

            trn(wvln) = np.exp(-(kabs_o2(wvln) * path_o2 / mu0)**a),

        where 'kabs_o2' denotes the oxygen absorption coefficients
        in cm-1, 'path_o2' is the oxygen absorption path given in cm,
        'mu0' is the cosine of the solar zenith angle and a is an
        empirical exponent (equal to 0.5641 for the molecular oxygen).

        Receive:

            wvln : array-like, shape (nwvln?,)
                wavelengths in nanometers
            mu0 : array-like, shape (ngeo?,)
                cosines of the solar zenith angle

        Return:

            trn : array-like, shape (ngeo?, nwvln?)
                oxygen transmittance for every geometry and wavelength

        Raise:

            ValueError
                if 'wvln' or 'mu0' have invalid shapes
        """

        # Ensure shape of the input arguments.
        if len(np.shape(wvln)) > 1:
            raise ValueError("'wvln' must be 0- or 1-dimensional")
        if len(np.shape(mu0)) > 1:
            raise ValueError("'mu0' must be 0- or 1-dimensional")

        # Compute the absorption coefficients for oxygen at the given input
        # wavelengths by using linear interpolation.
        oxygen_coef = np.atleast_1d(np.interp(wvln, *self.abscoef[[0, 4]]))
        mu0 = np.atleast_1d(mu0)[:, None]

        # Declare the oxygen path and the oxygen exponent as constants.
        oxygen_path = 0.209 * 173200
        oxygen_exp = 0.5641

        trn = np.exp(-(oxygen_coef * oxygen_path / mu0)**oxygen_exp)
        return np.squeeze(trn)

