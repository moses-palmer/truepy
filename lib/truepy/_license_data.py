# coding=utf-8
'''
truepy
Copyright (C) 2014 Moses Palmér

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
'''

from datetime import datetime


class LicenseData(object):
    """
    A class representing a license with a validity window and meta data.
    """

    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'

    @property
    def not_before(self):
        """The notBefore timestamp of this license"""
        return self._not_before

    @property
    def not_after(self):
        """The notAfter timestamp of this license"""
        return self._not_after

    @property
    def issued(self):
        """The issued timestamp of this license"""
        return self._issued

    @property
    def issuer(self):
        """The license issuer distinguished name"""
        raise NotImplemented()

    @property
    def holder(self):
        """The license holder distinguished name"""
        raise NotImplemented()

    @property
    def subject(self):
        """The license subject"""
        raise NotImplemented()

    @property
    def consumer_type(self):
        """The type of entity to which this license is issued"""
        raise NotImplemented()

    @property
    def information(self):
        """Generic information about this license"""
        raise NotImplemented()

    @property
    def extra(self):
        """The license extra data"""
        raise NotImplemented()

    def __init__(self, not_before, not_after, issued = None, issuer = None,
            holder = None, subject = None, consumer_type = None,
            information = None, extra = None):
        """
        Creates a new license data object.

        Any timestamps passed must be either instances of datetime.datetime, or
        strings parsable by License.TIMESTAMP_FORMAT; the timezone is assumed to
        be UTC.

        @param not_before, not_after
            The validity window. not_before must be strictly before not_after.
        @param issued
            The timestamp when this license was issued. This defaults to
            not_before.
        @param issuer, holder
            The issuer and holder of this certificate. These must be strings
            parsable by truepy.Name() or instances of truepy.Name.
        @param subject, consumer_type, information
            Free-form string data to associate with the license.
        @param extra
            Any type of data to store in the license. If this is not a string,
            it will be JSON serialised.
        """
        def timestamp(v):
            if isinstance(v, datetime):
                return v
            else:
                return datetime.strptime(v + ' UTC',
                    self.TIMESTAMP_FORMAT + ' %Z')

        self._not_before = timestamp(not_before)
        self._not_after = timestamp(not_after)
        if self._not_before >= self._not_after:
            raise ValueError('%s is not before %s',
                self._not_before, self._not_after)
        self._issued = timestamp(issued or not_before)
