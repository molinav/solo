from __future__ import division
import os.path
import numpy as np


def radtran(geo, atm, albedo, wvln=None, squeeze=True, coupling=False):
    """Return the BOA irradiances based on an atmosphere and geometry.

    Receive:

        geo : Geometry
            an instance of Geometry containing the relevant information
            of the geometric parameters
        atm : Atmosphere
            an instance of Atmosphere containing the relevant information
            of the atmospheric components
        albedo : array-like, shape (nwvln?,)
            surface albedo
        wvln : array-like, shape (nwvln?,), optional
            wavelengths in nanometers (default None, which means that
            the wavelengths are taken from the same file where the TOA
            irradiance is stored)
        squeeze : bool, optional
            if True, remove length-1 axes from the output arrays
            (default True)
        coupling : bool, optional
            if True, include Rayleigh-aerosol coupling effect
            (default False)

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
            if 'wvln' and 'albedo' have invalid shapes or cannot be
            broadcasted
        TypeError
            if 'squeeze' or 'coupling' are not boolean flags
    """

    # Read the TOA irradiance as a function of the wavelength.
    path = os.path.join(os.path.dirname(__file__), "dat", "kurucz.dat")
    wvln0, irr0 = np.loadtxt(path).T

    # Ensure consistency of the input arguments.
    if wvln is None:
        wvln = wvln0
    if len(np.shape(wvln)) > 1:
        raise ValueError("'wvln' must be 0- or 1-dimensional")
    if len(np.shape(albedo)) > 1:
        raise ValueError("'albedo' must be 0- or 1-dimensional")
    if not isinstance(squeeze, bool):
        raise TypeError("'squeeze' must be a bool")
    try:
        wvln, albedo = np.broadcast_arrays(wvln, albedo)
    except ValueError as err:
        err.__cause__ = None
        err.args = ("cannot broadcast 'wvln' and 'albedo to a single shape'",)
        raise err

    # Convert wavelengths from nanometers to microns and adjust the TOA
    # irradiance to the actual Sun-Earth distance.
    wvln_um = 1E-3 * wvln
    irr0 = irr0 * geo.geometric_factor(squeeze=False)

    # Compute the transmittance due to Rayleigh and aerosols.
    args = [wvln_um, geo.mu0, False, True, coupling]
    tglb_mix, tdir_mix, tdif_mix, atm_alb = atm.trn_mixture(*args)
    atm_alb = atm_alb[:, None, :]

    # Compute the transmittance due to gas absorption.
    args = [wvln, geo.mu0, False]
    tdir_wat = atm.trn_water(*args)
    tdir_ozo = atm.trn_ozone(*args)
    tdir_oxy = atm.trn_oxygen(*args)
    tdir_gas = tdir_wat * tdir_ozo * tdir_oxy

    # Compute the amplification factor for the BOA global irradiance.
    amp_factor = 1. / (1. - albedo * atm_alb)

    # Compute the BOA global, direct and diffuse irradiances.
    mu0 = np.atleast_1d(geo.mu0)[None, :, None]
    irr_glb = irr0 * mu0 * tglb_mix * tdir_gas * amp_factor
    irr_dir = irr0 * tdir_mix * tdir_gas
    irr_dif = irr_glb - irr_dir * mu0

    # If requested, squeeze the length-1 axes from the output arrays.
    out = (irr_glb, irr_dir, irr_dif)
    if bool(squeeze):
        out = tuple(np.squeeze(x) for x in out)
    return out

