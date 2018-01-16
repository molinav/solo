from __future__ import division
import os.path
import numpy as np


def radtran(geo, atm, wvln=None, coupling=True):
    """Return the BOA irradiances based on an atmosphere and geometry.

    Receive:

        geo : Geometry
            an instance of Geometry containing the relevant information
            of the geometric parameters
        atm : Atmosphere
            an instance of Atmosphere containing the relevant information
            of the atmospheric components
        wvln : array-like, shape (nwvln?,), optional
            wavelengths in nanometers (default None, which means that
            the wavelengths are taken from the same file where the TOA
            irradiance is stored)
        coupling : bool, optional
            if True, include Rayleigh-aerosol coupling effect
            (default True)

    Return:

        irr_glb : array-like, shape (nscen?, ngeo?, nwvln?)
            BOA global irradiance for every scenario, geometry and
            wavelength
        irr_dir : array-like, shape (nscen?, ngeo?, nwvln?)
            BOA direct irradiance for every scenario, geometry and
            wavelength
        irr_dif : array-like, shape (nscen?, ngeo?, nwvln?)
            BOA diffuse irradiance for every scenario, geometry and
            wavelength

    Raise:

        ValueError
            if 'wvln' has an invalid shape
        TypeError
            if 'coupling' is not a boolean flag
    """

    # Read the TOA irradiance as a function of the wavelength.
    path = os.path.join(os.path.dirname(__file__), "dat", "kurucz.dat")
    wvln0, irr0 = np.loadtxt(path).T

    # Ensure consistency of the input arguments.
    if wvln is None:
        wvln = wvln0
    if len(np.shape(wvln)) > 1:
        raise ValueError("'wvln' must be 0- or 1-dimensional")

    # Convert wavelengths from nanometers to microns and adjust the TOA
    # irradiance to the actual Sun-Earth distance.
    wvln_um = 1E-3 * wvln
    irr0 = irr0 * np.atleast_1d(geo.geometric_factor())[:, None]

    # Compute the transmittance due to Rayleigh and aerosols.
    args = [wvln_um, geo.mu0, True, coupling]
    tglb_mix, tdir_mix, tdif_mix, atm_alb = atm.trn_mixture(*args)
    atm_rho = np.atleast_1d(atm.rho)[:, None]

    # Compute the transmittance due to gas absorption.
    args = [wvln, geo.mu0]
    tdir_wat = atm.trn_water(*args)
    tdir_ozo = atm.trn_ozone(*args)
    tdir_oxy = atm.trn_oxygen(*args)
    tdir_gas = tdir_wat * tdir_ozo * tdir_oxy

    # Compute the amplification factor for the BOA global irradiance.
    amp_factor = 1. / (1. - atm_rho * atm_alb)

    # Compute the BOA global, direct and diffuse irradiances.
    mu0 = np.atleast_1d(geo.mu0)[:, None]
    irr_glb = irr0 * mu0 * tglb_mix * tdir_gas * amp_factor
    irr_dir = irr0 * tdir_mix * tdir_gas
    irr_dif = irr_glb - irr_dir * mu0

    # If requested, squeeze the length-1 axes from the output arrays.
    out = (irr_glb, irr_dir, irr_dif)
    return out

