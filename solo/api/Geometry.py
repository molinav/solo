from __future__ import division
from collections import namedtuple
import numpy as np


ATTRS = ["day", "lat", "lon", "sza", "mu0"]
DAY_TO_RAD = 2. * np.pi / 365.


class Geometry(namedtuple("Geometry", ATTRS)):
    """Class to define the geometric properties of the atmospheric view.

    Every instance allows the access to the following properties:

        ngeo : int
            number of scenarios

        day : array-like, shape (ngeo?,)
            Julian day ranged from 1 to 366

        day_angle : array-like, shape (ngeo?,)
            angle between the Earth-Sun line on 1st January and the same
            line for the Julian days corresponding to the scenarios,
            ranged from 0 to 2 * np.pi rad

        lat : array-like, shape (ngeo?,)
            latitude at the viewing positions in radians, ranged from
            -np.pi / 2 to +np.pi / 2 rad

        lon : array-like, shape (ngeo?,)
            longitude at the viewing positions in radians, ranged from
            -np.pi to +np.pi rad

        sza : array-like, shape (ngeo?,)
            solar zenith angles in radians, ranged from 0 to +np.pi rad

        mu0 : array-like, shape (ngeo?,)
            cosines of the solar zenith angle, ranged from -1 to +1
    """

    def __new__(cls, lat, lon, sza, day, mode="deg"):
        """Return a new instance of Geometry.

        Receive:

            lat : array-like, (ngeo?,)
                latitude at the viewing positions
            lon : array-like, (ngeo?,)
                longitude at the viewing positions
            sza : array-like, (ngeo?,)
                solar zenith angles
            day : array-like, (ngeo?,)
                Julian day
            mode : str
                if 'deg', input angles are provided in degrees; if 'rad',
                input angles are given in radians; otherwise, and error
                is raised (default 'deg'); note that the instance always
                stores the angles in radians

        Return:

            geo : Geometry
                instance of Geometry based on the input parameters

        Raise:

            AttributeError
                if input arguments have inconsistent or wrong shapes
            ValueError
                if mode is not equal to 'deg' or 'rad' or the input
                arguments are out of range
        """

        # Declare constructor arguments.
        args = [day, lat, lon, sza]

        # Ensure that the input arguments have consistent shapes and sizes.
        set_shapes = set(np.shape(x) for x in args if x is not None)
        if len(set_shapes) > 1:
            raise AttributeError("size mismatch among input arguments")
        set_shapes = list(set_shapes)[0]
        if len(set_shapes) > 1:
            raise AttributeError("input arguments must be 0- or 1-dimensional")

        # Check that mode receives a valid value ('rad' or 'deg').
        if mode.lower() == "rad":
            to_radians = lambda x: x
        elif mode.lower() == "deg":
            to_radians = np.radians
        else:
            raise ValueError("invalid value for 'mode': {}".format(mode))

        # Check that the Julian days are within valid range.
        if np.any(day < 1) or np.any(day > 366):
            raise ValueError("Julian days out of range")

        # Check that the latitudes are within valid range.
        if lat is not None:
            lat = to_radians(lat)
            if np.any(np.abs(lat) > np.pi / 2):
                raise ValueError("latitude values out of range")

        # Check that the longitudes are within valid range.
        if lon is not None:
            lon = to_radians(lon)
            if np.any(np.abs(lon) > np.pi):
                raise ValueError("longitude values out of range")

        # Check that the solar zenith angles are within valid range.
        if sza is not None:
            sza = to_radians(sza)
            if np.any(np.abs(sza - np.pi / 2) > np.pi / 2):
                raise ValueError("solar zenith angle values out of range")

        # Compute the cosine of the solar zenith angle.
        mu0 = np.cos(sza)

        # Return the new instance.
        geo = super(Geometry, cls).__new__(cls, day, lat, lon, sza, mu0)
        return geo

    @property
    def day_angle(self):
        """Return the day angle for every Julian day.

        The day angle is defined as the angle between the Earth-Sun line
        on 1st January and the same line for the Julian days
        corresponding to the scenarios.

        Return:

            day_angle : array-like, shape (ngeo?,)
                day angle for every scenario's Julian day
        """

        return (self.day - 1) * DAY_TO_RAD

    @property
    def ngeo(self):
        """Return the number of geometries stored within the instance."""

        shp = np.shape(self.mu0)
        return shp[0] if shp else 1

    def geometric_factor(self, squeeze=True):
        """Return the factor used to correct the solar TOA irradiance.

        The solar TOA irradiance E0 is normally provided for a constant
        Earth-Sun distance, but this distance changes as a function of
        the day number, so that

            E(day) = E0 * (r0 / r(day))**2

        where E(day) is the solar TOA irradiance for the given days, E0
        is the solar TOA irradiance for the reference day, r(day) is the
        Sun-Earth distance for the given days, and r0 is the Sun-Earth
        distance for the reference day. This function returns the
        geometric factor (r0 / r(day))**2 when E0 and r0 are defined for
        a Sun-Earth distance of 1 AU.

        Receive:

            squeeze : bool, optional
                if True, remove length-1 axes from the output arrays
                (default True)

        Return:

            geo_factor : array-like, shape (ngeo?,)
                geometric factor for every scenario
        """

        # Ensure that 'squeeze' is a bool flag.
        if not isinstance(squeeze, bool):
            raise TypeError("'squeeze' must be a bool")

        # Define the coefficients of the Fourier series.
        c = [1.00011, 0.03422, 0.00128, 0.000719, 0.000077]

        day_ang1 = self.day_angle
        day_ang2 = day_ang1 * 2

        geo_factor = c[0] + c[1] * np.cos(day_ang1) + c[2] * np.sin(day_ang1) \
                          + c[3] * np.cos(day_ang2) + c[4] * np.sin(day_ang2)

        if bool(squeeze):
            return np.squeeze(geo_factor)
        else:
            return np.atleast_1d(geo_factor)[None, :, None]

    def declination(self):
        """Return the Sun declination for the current Geometry instance.

        Return:

            dec : array-like, shape (ngeo?,)
                Sun declination for every scenario in radians
        """

        # Compute the day of the year in radians.
        ett1 = self.day * DAY_TO_RAD
        ett2 = 2. * ett1
        ett3 = 3. * ett1

        # Define the coefficients of the Fourier series.
        c = [0.006918, -0.399912, 0.070257, -0.006758,
             0.000907, -0.002697, 0.001480]

        # Compute the declination in radians.
        dec = c[0] + c[1] * np.cos(ett1) + c[2] * np.sin(ett1)                \
                   + c[3] * np.cos(ett2) + c[4] * np.sin(ett2)                \
                   + c[5] * np.cos(ett3) + c[6] * np.sin(ett3)

        return dec

