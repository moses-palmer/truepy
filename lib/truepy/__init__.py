# coding: utf-8
# truepy
# Copyright (C) 2014-2020 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.


from xml.etree.ElementTree import tostring as _tostring
from xml.etree.ElementTree import fromstring


import sys
if sys.version_info.major > 2:
    def tostring(e):
        return str(_tostring(e), 'ascii')
else:
    tostring = _tostring

from ._info import *
from ._license_data import LicenseData
from ._license import License
from ._name import Name
