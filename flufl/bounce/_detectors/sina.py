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

"""sina.com bounces"""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Sina',
    ]


import re

from email.iterators import body_line_iterator
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


acre = re.compile(r'<(?P<addr>[^>]*)>')



@implementer(IBounceDetector)
class Sina:
    """sina.com bounces"""

    def process(self, msg):
        """See `IBounceDetector`."""
        if msg.get('from', '').lower() != 'mailer-daemon@sina.com':
            return NoFailures
        if not msg.is_multipart():
            return NoFailures
        # The interesting bits are in the first text/plain multipart.
        part = None
        try:
            part = msg.get_payload(0)
        except IndexError:
            pass
        if not part:
            return NoFailures
        addresses = set()
        for line in body_line_iterator(part):
            mo = acre.match(line)
            if mo:
                addresses.add(mo.group('addr').encode('us-ascii'))
        return NoTemporaryFailures, addresses
