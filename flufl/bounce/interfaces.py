# Copyright (C) 2011 by Barry A. Warsaw
#
# This file is part of flufl.bounce
#
# flufl.bounce is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# flufl.bounce is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.bounce.  If not, see <http://www.gnu.org/licenses/>.

"""Interfaces."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'IBounceDetector',
    ]


from zope.interface import Interface



class IBounceDetector(Interface):
    """Detect a bounce in an email message."""

    def process(self, msg):
        """Scan an email message looking for bounce addresses.

        :param msg: An email message.
        :type msg: `Message`
        :return: A 2-tuple of the detected temporary and permanent bouncing
            addresses.  Both elements of the tuple are sets of string
            email addresses.  Not all detectors can tell the difference
            between temporary and permanent failures, in which case, the
            addresses will be considered to be permanently bouncing.
        :rtype: (set of strings, set of string)
        """
