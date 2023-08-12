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
"""Geometry class encapsulation."""

from collections import namedtuple
import numpy as np


ATTRS = ["day", "sec", "lat", "lon", "sza", "mu0"]

# Define conversion factors.
DAY_TO_RAD = 2. * np.pi / 365.
HOUR_TO_RAD = np.pi / 12.
HOUR_TO_SEC = 3600.


class Geometry(namedtuple("Geometry", ATTRS)):
    r"""Class to define the geometric properties of the atmospheric view.

    During instance creation, the ``mode`` variable must be selected
    from `{'deg', 'rad'}` to indicate if the variables ``lat``, ``lon``
    and ``sza`` are provided in degrees or radians, respectively. Once
    the instance is created, all these variables are stored in radians.

    Attributes
    ----------

    day : array-like
        Julian day, ranged from 1 to 366

    sec : array-like
        UTC time in seconds, ranged from 0 to 86399

    lat : array-like
        latitude at the viewing positions in radians,
        ranged from :math:`-\pi/2` to :math:`+\pi/2` rad

    lon : array-like
        longitude at the viewing positions in radians,
        ranged from :math:`-\pi` to :math:`+\pi` rad

    sza : array-like
        solar zenith angles in radians,
        ranged from :math:`0` to :math:`+\pi` rad

    mu0 : array-like
        cosine of the solar zenith angles,
        ranged from :math:`-1` to :math:`+1`
    """

    def __new__(cls, day, sec=None,  # pylint: disable=too-many-arguments
                lat=None, lon=None, sza=None, mode="deg"):
        """Return a new :class:`Geometry` instance."""

        # Declare constructor arguments.
        args = [day, sec, lat, lon, sza]

        # Ensure that the input arguments have consistent shapes and sizes.
        set_shapes = set(np.shape(x) for x in args if x is not None)
        if len(set_shapes) > 1:
            raise ValueError("size mismatch among input arguments")
        set_shapes = list(set_shapes)[0]
        if len(set_shapes) > 1:
            raise ValueError("input arguments must be 0- or 1-dimensional")

        # Check that mode receives a valid value ('rad' or 'deg').
        if mode.lower() == "rad":
            to_radians = lambda x: x
        elif mode.lower() == "deg":
            to_radians = np.radians
        else:
            raise ValueError("invalid value for 'mode': {0}".format(mode))

        # Check that the Julian days are within valid range.
        if np.any(day < 1) or np.any(day > 366):
            raise ValueError("Julian days out of range")
        day = np.atleast_1d(day).astype(int)

        # Check that the UTC seconds are within valid range.
        if sec is not None:
            if np.any(sec < 0) or np.any(sec > 86399):
                raise ValueError("UTC seconds out of range")
            sec = np.atleast_1d(sec).astype(int)

        # Check that the latitudes are within valid range.
        if lat is not None:
            lat = np.atleast_1d(to_radians(lat))
            if np.any(np.abs(lat) > np.pi / 2):
                raise ValueError("latitude values out of range")

        # Check that the longitudes are within valid range.
        if lon is not None:
            lon = np.atleast_1d(to_radians(lon))
            if np.any(np.abs(lon) > np.pi):
                raise ValueError("longitude values out of range")

        # Check that the solar zenith angles are within valid range.
        if sza is not None:
            sza = np.atleast_1d(to_radians(sza))
            if np.any(np.abs(sza - np.pi / 2) > np.pi / 2):
                raise ValueError("solar zenith angle values out of range")
        else:
            args = [cls, day, sec, lat, lon, sza, None]
            geo = super(Geometry, cls).__new__(*args)
            sza = geo.compute_sza()

        # Compute the cosine of the solar zenith angle.
        mu0 = np.cos(sza)

        # Return the new instance.
        args = [cls, day, sec, lat, lon, sza, mu0]
        geo = super(Geometry, cls).__new__(*args)
        return geo

    def __eq__(self, other):
        """Return if two :class:`Geometry` instances are equal."""

        result = True
        if not isinstance(other, Geometry):
            result = False
        elif self.ngeo != other.ngeo:
            result = False
        elif not np.allclose(self.day, other.day, equal_nan=True):
            result = False
        elif not np.allclose(self.sza, other.sza, equal_nan=True):
            result = False
        elif not np.allclose(self.mu0, other.mu0, equal_nan=True):
            result = False
        else:
            for key in ("sec", "lat", "lon"):
                values = getattr(self, key), getattr(other, key)
                if any(x is None for x in values):
                    result = all(x is None for x in values)
                else:
                    result = np.allclose(values[0], values[1], equal_nan=True)
                if not result:
                    break
        return result

    @property
    def ngeo(self):
        """Number of geometries stored in the instance."""

        shp = np.shape(self.mu0)
        return shp[0] if shp else 1

    @property
    def day_angle(self):
        r"""Day angle for every geometry's Julian day.

        The day angle is defined as the angle between the Earth-Sun
        line on 1st January and the same line for the Julian days
        corresponding to the instance geometries, ranged from
        :math:`0` to :math:`2\pi` rad
        """

        return (self.day - 1) * DAY_TO_RAD

    def geometric_factor(self):
        r"""Return geometric factor used to correct the solar TOA irradiance.

        The solar TOA irradiance :math:`E_0` is normally provided for a
        reference Earth-Sun distance, but this distance changes as a
        function of the day number :math:`n_\text{day}`, so that

        .. math::
            E(n_\text{day}) =
                E_0 \times \left(\dfrac{r_0}{r(n_\text{day})}\right)^2

        where :math:`E(n_\text{day})` is the solar TOA irradiance for
        the given days, :math:`E_0` is the solar TOA irradiance for the
        reference day, :math:`r(n_\text{day})` is the Sun-Earth distance
        for the given days, and :math:`r_0` is the Sun-Earth distance
        for the reference day. This function returns the geometric
        factor :math:`(r_0 / r(n_\text{day}))^2` when :math:`E_0`
        and :math:`r_0` are defined for a Sun-Earth distance of 1 AU.

        Returns
        -------

        geo_factor : array-like
            geometric factor, with shape ``(ngeo,)``,
            for every geometry
        """

        # Define the coefficients of the Fourier series.
        c = [1.00011, 0.03422, 0.00128, 0.000719, 0.000077]

        day_ang1 = self.day_angle
        day_ang2 = day_ang1 * 2

        return (+ c[0]
                + c[1] * np.cos(day_ang1) + c[2] * np.sin(day_ang1)
                + c[3] * np.cos(day_ang2) + c[4] * np.sin(day_ang2))

    def declination(self):
        """Return the Sun declination for the :class:`Geometry` instance.

        Returns
        -------

        dec : array-like
            Sun declination in radians, with shape ``(ngeo,)``,
            for every geometry
        """

        # Compute the day of the year in radians.
        ett1 = self.day * DAY_TO_RAD
        ett2 = 2. * ett1
        ett3 = 3. * ett1

        # Define the coefficients of the Fourier series.
        c = [0.006918, -0.399912, 0.070257, -0.006758,
             0.000907, -0.002697, 0.001480]

        # Compute the declination in radians.
        return (+ c[0]
                + c[1] * np.cos(ett1) + c[2] * np.sin(ett1)
                + c[3] * np.cos(ett2) + c[4] * np.sin(ett2)
                + c[5] * np.cos(ett3) + c[6] * np.sin(ett3))

    def equation_of_time(self):
        r"""Return the equation of time for the :class:`Geometry` instance.

        The equation of time (:math:`\text{ET}`) computes the difference
        between the true solar time (:math:`\text{TST}`), i.e. the time
        which tracks the diurnal motion of the Sun, and the mean solar
        time (:math:`\text{MST}`), i.e. the time which tracks the motion
        of a theoretical Sun with noons always 24 hours apart, so that

        .. math::
            \text{TST}(n_\text{day}) =
                \text{MST}(n_\text{day}) + \text{ET}(n_\text{day})

        Returns
        -------

        eot : array-like
            equation of time values in radians, with shape ``(ngeo,)``,
            for every geometry
        """

        # Compute the day of the year in radians.
        ett1 = self.day * DAY_TO_RAD
        ett2 = 2. * ett1

        # Define the coefficients of the Fourier series.
        c = [0.000075, 0.001868, -0.032077, -0.014615, -0.040849]

        # Compute the equation of time in radians.
        return (+ c[0]
                + c[1] * np.cos(ett1) + c[2] * np.sin(ett1)
                + c[3] * np.cos(ett2) + c[4] * np.sin(ett2))

    def compute_sza(self):
        """Return the solar zenith angles for the :class:`Geometry` instance.

        In case there are already solar zenith angles, they are just
        returned. If not, they are computed based on the datetime and
        the geolocation (latitude, longitude).

        Returns
        -------

        sza : array-like
            solar zenith angles in radians, with shape ``(ngeo,)``,
            for every geometry

        Raises
        ------

        ValueError
            if the latitude, longitude or datetime is missing
        """

        # Ensure that the solar zenith angle is not already computed, or that
        # the geolocation attributes are not missing.
        if self.sza is not None:
            return self.sza
        if self.sec is None:
            raise ValueError("UTC seconds missing")
        if self.lat is None:
            raise ValueError("latitude values missing")
        if self.lon is None:
            raise ValueError("longitude values missing")

        # Compute the mean solar time (MST) as a function of the UTC time and
        # the time shift due to the geographic longitude.
        mst = self.sec / HOUR_TO_SEC + self.lon / HOUR_TO_RAD

        # Compute the true solar time (TST) as a function of the MST and the
        # equation of time (EOT) converted from angle to time units.
        tst = mst + self.equation_of_time() / HOUR_TO_RAD
        hour_angle = (tst - 12.) * HOUR_TO_RAD

        # Compute `mu0` and the solar zenith angle.
        dec = self.declination()
        mu0 = (+ np.sin(self.lat) * np.sin(dec)
               + np.cos(self.lat) * np.cos(dec) * np.cos(hour_angle))
        sza = np.arccos(mu0)

        return sza

    @staticmethod
    def from_file(path):
        """Create :class:`Geometry` instance from file.

        Parameters
        ----------

        path : str
            location of input file

        Returns
        -------

        geo : Geometry
            new :class:`Geometry` instance based on the input file

        Raises
        ------

        ValueError
            if the input file does not have a valid format
        """

        def timestr2num(txt):
            """Converter function from time strings to seconds."""

            # Try to split the hours, minutes and seconds from time string.
            try:
                nums = list(map(int, txt.decode().split(":")))
            except ValueError:
                raise ValueError("invalid UTC time format")
            # If there is only one number, it is assumed as seconds.
            if len(nums) == 1:
                return nums[0]
            # If there are 2 or three numbers, they are assumed as
            # [hours, minutes, (seconds)].
            if len(nums) in [2, 3]:
                return sum(x * y for x, y in zip(nums, [3600, 60, 1]))
            # Any other case is not valid.
            raise ValueError("invalid UTC time format")

        # Define the possible list of input arguments depending on its number.
        keys = {2: ["day", "sza"], 4: ["day", "sec", "lat", "lon"]}

        # Try to open the file assuming that all the values are numbers.
        # Otherwise, raise an error.
        try:
            data = np.atleast_2d(np.loadtxt(path))
            args = data.ravel() if data.shape[0] == 1 else data.T
        # If it does not work, try to parse the second column as a timestring.
        except ValueError:
            try:
                converters = {1: timestr2num}
                data = np.atleast_2d(np.loadtxt(path, converters=converters))
                args = data.ravel() if data.shape[0] == 1 else data.T
            # If it does not work, it may be a single geometry in column form.
            except (ValueError, IndexError):
                try:
                    data = np.loadtxt(path, dtype=bytes)
                    if data.shape == (4,):
                        data = np.atleast_2d(data)
                        args = [int(data[0, 0]), timestr2num(data[0, 1]),
                                float(data[0, 2]), float(data[0, 3])]
                    else:
                        raise ValueError("invalid file format")
                # If nothing works, then the file cannot be imported.
                except ValueError:
                    raise ValueError("invalid file format")

        # Parse the columns into a possible combination of input arguments,
        # otherwise raise an error.
        try:
            kwargs = dict(zip(keys[data.shape[1]], args))
        except KeyError:
            raise ValueError("invalid file format")

        return Geometry(**kwargs)
