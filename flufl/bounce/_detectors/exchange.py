# Copyright (C) 2002-2012 by Barry A. Warsaw
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

"""Recognizes (some) Microsoft Exchange formats."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Exchange',
    ]


import re

from email.iterators import body_line_iterator
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


scre = re.compile('did not reach the following recipient')
ecre = re.compile('MSEXCH:')
a1cre = re.compile('SMTP=(?P<addr>[^;]+); on ')
a2cre = re.compile('(?P<addr>[^ ]+) on ')



@implementer(IBounceDetector)
class Exchange:
    """Recognizes (some) Microsoft Exchange formats."""

    def process(self, msg):
        """See `IBounceDetector`."""
        addresses = set()
        it = body_line_iterator(msg)
        # Find the start line.
        for line in it:
            if scre.search(line):
                break
        else:
            return NoFailures
        # Search each line until we hit the end line.
        for line in it:
            if ecre.search(line):
                break
            mo = a1cre.search(line)
            if not mo:
                mo = a2cre.search(line)
            if mo:
                # For Python 3 compatibility, the API requires bytes
                address = mo.group('addr').encode('us-ascii')
                addresses.add(address)
        return NoTemporaryFailures, set(addresses)
