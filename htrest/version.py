#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  HtREST - Heliotherm heat pump REST API
#  Copyright (C) 2019  Daniel Strigl

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" TODO """


class Version:
    """ Object which encapsulates the version information.

    :param package: Name of the package.
    :type package: str
    :param major: The major version number.
    :type major: int
    :param minor: The minor version number.
    :type minor: int
    :param patch: The patch version number.
    :type patch: int
    """

    def __init__(self, package: str, major: int, minor: int, patch: int) -> None:
        self.package = package
        self.major = major
        self.minor = minor
        self.patch = patch

    def short(self) -> str:
        """" Return a string in canonical short version format ``<major>.<minor>.<patch>``.

        :returns: A string in canonical short version format.
        :rtype: ``str``
        """
        return "{:d}.{:d}.{:d}".format(self.major, self.minor, self.patch)

    def __str__(self) -> str:
        """ Return a string representation of the object.

        :returns: A string representation of this object.
        :rtype: ``str``
        """
        return "[{}, version {}]".format(self.package, self.short())


version = Version("HtREST", 1, 0, 0)
""" TODO """
# version.__name__ = "HtREST"
