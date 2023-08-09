#! /usr/bin/env python
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
"""radtran function encapsulation."""

from __future__ import print_function
from __future__ import division
import sys
import os.path
import numpy as np


def radtran(geo, atm, wvln=None, coupling=True):
    """Return the BOA irradiances based on an atmosphere and geometry.

    Parameters
    ----------

    geo : Geometry
        a :class:`~solo.api.Geometry` instance with the
        relevant geometric parameters

    atm : Atmosphere
        an :class:`~solo.api.Atmosphere` instance with the
        relevant atmospheric components

    wvln : array-like, optional
        wavelengths in nanometers, with shape ``(nwvln,)``; if
        not given, the wavelengths are taken from the same file
        where the TOA irradiances are stored

    coupling : bool, optional
        if True, include Rayleigh-aerosol coupling effect

    Returns
    -------

    irr_glb : array-like
        BOA global irradiance, with shape ``(nscen, nwvln)``,
        for every input scenario and wavelength

    irr_dir : array-like
        BOA direct irradiance, with shape ``(nscen, nwvln)``,
        for every input scenario and wavelength

    irr_dif : array-like
        BOA diffuse irradiance, with shape ``(nscen, nwvln)``,
        for every input scenario and wavelength

    Raises
    ------

    ValueError
        if ``wvln`` has an invalid shape

    TypeError
        if ``coupling`` is not a boolean flag
    """

    # Read the TOA irradiance as a function of the wavelength.
    path = os.path.join(os.path.dirname(__file__), "dat", "kurucz.dat")
    wvln0, irr0 = np.loadtxt(path).T

    # Ensure consistency of the input arguments.
    wvln = np.atleast_1d(wvln0 if wvln is None else wvln)
    if np.ndim(wvln) > 1:
        raise ValueError("'wvln' must be 0- or 1-dimensional")

    # Convert wavelengths from nanometers to microns and adjust the TOA
    # irradiance to the actual Sun-Earth distance.
    wvln_um = 1E-3 * wvln
    irr0 = irr0 * geo.geometric_factor()[:, None]

    # Compute the transmittance due to Rayleigh and aerosols.
    args = [wvln_um, geo.mu0, True, coupling]
    tglb_mix, tdir_mix, _tdif_mix, atm_alb = atm.trn_mixture(*args)

    # Compute the transmittance due to gas absorption.
    args = [wvln, geo.mu0]
    tdir_wat = atm.trn_water(*args)
    tdir_ozo = atm.trn_ozone(*args)
    tdir_oxy = atm.trn_oxygen(*args)
    tdir_gas = tdir_wat * tdir_ozo * tdir_oxy

    # Compute the amplification factor for the BOA global irradiance.
    amp_factor = 1. / (1. - atm.rho[:, None] * atm_alb)

    # Compute the BOA global, direct and diffuse irradiances.
    mu0 = geo.mu0[:, None]
    irr_glb = irr0 * mu0 * tglb_mix * tdir_gas * amp_factor
    irr_dir = irr0 * tdir_mix * tdir_gas
    irr_dif = irr_glb - irr_dir * mu0

    # If requested, squeeze the length-1 axes from the output arrays.
    out = (irr_glb, irr_dir, irr_dif)
    return out


def _main(argv=None):
    """Main script function."""

    import getopt
    from . api import Geometry
    from . api import Atmosphere

    # Read arguments and options.
    argv = argv if argv is not None else sys.argv[1:]
    optkeys = ["geo=", "atm=", "out=", "no-coupling"]
    optlist, _ = getopt.getopt(argv, "", optkeys)

    # Parse --geo option.
    geo = [x[1] for x in optlist if x[0] == "--geo"]
    if not geo:
        print("Error: missing --geo option")
        sys.exit(1)
    if len(geo) != 1:
        print("Error: multiple --geo options")
        sys.exit(1)
    try:
        geo = Geometry.from_file(geo[0])
    except Exception as err:  # pylint: disable=broad-except
        print("{}\nError: wrong Geometry input file".format(err))
        sys.exit(1)

    # Parse --atm option.
    atm = [x[1] for x in optlist if x[0] == "--atm"]
    if not atm:
        print("Error: missing --atm option")
        sys.exit(2)
    if len(atm) != 1:
        print("Error: multiple --atm options")
        sys.exit(2)
    try:
        atm = Atmosphere.from_file(atm[0])
    except Exception as err:  # pylint: disable=broad-except
        print("{}\nError: wrong Atmosphere input file".format(err))
        sys.exit(2)

    # Parse --out option.
    out = [x[1] for x in optlist if x[0] == "--out"]
    if not out:
        print("Error: missing --out option")
        sys.exit(3)
    if len(out) != 1:
        print("Error: multiple --out options")
        sys.exit(3)
    out = str(out[0])
    out_cut = os.path.splitext(out)
    out_glb = "".join([out_cut[0], "_glb", out_cut[1]])
    out_dir = "".join([out_cut[0], "_dir", out_cut[1]])
    out_dif = "".join([out_cut[0], "_dif", out_cut[1]])

    # Parse --no-coupling option.
    coupling = [x[1] for x in optlist if x[0] == "--no-coupling"]
    coupling = not bool(coupling)

    # Run the radiative transfer solver.
    irr_glb, irr_dir, irr_dif = radtran(geo, atm, None, coupling)

    # Export the results into text files.
    np.savetxt(out_glb, irr_glb.T, fmt="%+14.6E")
    np.savetxt(out_dir, irr_dir.T, fmt="%+14.6E")
    np.savetxt(out_dif, irr_dif.T, fmt="%+14.6E")


if __name__ == "__main__":
    sys.exit(_main())
